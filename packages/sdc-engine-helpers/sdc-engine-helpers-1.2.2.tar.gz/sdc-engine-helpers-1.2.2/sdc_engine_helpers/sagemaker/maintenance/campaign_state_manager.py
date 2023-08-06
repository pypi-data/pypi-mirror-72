"""
    Campaign state manager module
"""
from datetime import datetime
import sdc_helpers.utils as utils
import boto3
from sdc_engine_helpers.date_utils import DateUtils

class CampaignStateManager:
    """
        Given a database campaign object,

        1. get_state
            - call vendor API's to check if campaign needs to be updated
            OR
            - check if the campaign status in the database needs to be refreshed.
        2. update_state
            - call vendor API's to execute update workflow for campaign
            - update status of campaign in database

    """
    date_utils = DateUtils()
    # vendor
    vendor_solution_arn_path = 'TrainingJobName'
    vendor_campaign_arn_path = 'EndpointName'
    vendor_campaign_status_path = 'EndpointStatus'
    vendor_solution_status_path = 'TrainingJobStatus'
    # input data key in TrainingJob
    vendor_campaign_solution_arn_path = 'ProductionVariants.0.VariantName'

    campaign_statuses = {
        'running':['Creating', 'Updating', 'SystemUpdating', 'Deleting'],
        'updating': ['Updating'],
        'failed':['Failed', 'RollingBack'],
        'danger':['Failed'],
        'blocking':[
            'Creating',
            'Updating',
            'SystemUpdating',
            'Deleting',
            'Failed',
            'RollingBack'
        ],
        'stopped':['OutOfService'],
        'active':['InService']
    }

    solution_statuses = {
        'blocking': ['InProgress', 'Stopping', 'Failed', 'Stopped'],
        'success': ['Completed']
    }

    dataset_statuses = {
        'active': ['Active'],
        'blocking': ['Updating']
    }

    def __init__(self):
        self.sagemaker = boto3.client('sagemaker')

   # pylint: disable=invalid-name
    def sagemaker_create_model(self, TrainingJobName: str):
        """Create model from a trained model job using Sagemaker API"""
        model_name = TrainingJobName

        training_job_config = self.sagemaker.describe_training_job(
            TrainingJobName=TrainingJobName
        )

        primary_container = {
            'Image': training_job_config['AlgorithmSpecification']['TrainingImage'],
            'ModelDataUrl': training_job_config['ModelArtifacts']['S3ModelArtifacts']
        }

        _ = self.sagemaker.create_model(
            ModelName=model_name,
            ExecutionRoleArn=training_job_config['RoleArn'],
            PrimaryContainer=primary_container
        )

        return model_name

    def sagemaker_update_campaign(self, EndpointName: str, TrainingJobName: str):
        """
            (Call vendor API) Creates a endpoint config
            and updates endpoint with this config

            Args:
                EndpointName (str): name of sagemaker endpoint
                TrainingJobName (str): name of sagemaker training job

            Returns:
                dict: contains names of new created resources
        """
        endpoint_config_name = "{}-{}".format("Campaign", TrainingJobName)

        endpoint = self.sagemaker.describe_endpoint(
            EndpointName=EndpointName)

        ModelName = self.sagemaker_create_model(TrainingJobName=TrainingJobName)

        previous_endpoint_config = self.sagemaker.describe_endpoint_config(
            EndpointConfigName=endpoint['EndpointConfigName'])

        production_varients = previous_endpoint_config['ProductionVariants']
        # update the model name in production varients
        production_varients[0]['ModelName'] = ModelName
        production_varients[0]['VariantName'] = ModelName

        _ = self.sagemaker.create_endpoint_config(
            EndpointConfigName=endpoint_config_name,
            ProductionVariants=production_varients
        )

        _ = self.sagemaker.update_endpoint(
            EndpointName=EndpointName,
            EndpointConfigName=endpoint_config_name
        )

        return {
            'EndpointName': EndpointName,
            'TrainingJobName':TrainingJobName,
            'ModelName': ModelName
        }

    def get_vendor_solution_version_arn(self, vendor_solution: dict):
        """
            Get vendor solution version status

            args:
                vendor_solution (dict): Solution from vendor

            returns:
                status (str): vendor solution version status

        """

        return utils.dict_query(
            dictionary=vendor_solution,
            path=self.vendor_solution_arn_path
        )

    def get_vendor_campaign_solution_version_arn(self, vendor_campaign: dict):
        """
            Get vendor campaign version status

            args:
                vendor_campaign (dict): Campaign from vendor

            returns:
                status (str): vendor campaign version status

        """

        return utils.dict_query(
            dictionary=vendor_campaign,
            path=self.vendor_campaign_solution_arn_path
        )

    def get_vendor_solution_status(self, vendor_solution: dict):
        """
            Get vendor solution version status

            args:
                vendor_solution (dict): Solution from vendor

            returns:
                status (str): vendor solution version status

        """

        return utils.dict_query(
            dictionary=vendor_solution,
            path=self.vendor_solution_status_path
        )

    def get_vendor_campaign_status(self, vendor_campaign: dict):
        """
            Get vendor campaign version status

            args:
                vendor_campaign (dict): Campaign from vendor

            returns:
                status (str): vendor campaign version status

        """

        return utils.dict_query(
            dictionary=vendor_campaign,
            path=self.vendor_campaign_status_path
        )

    def get_state(self, *, campaign: dict, solution: dict) -> dict:
        """
            Get the current state to action an update, refresh or do nothing
            set of actions.

            Args:
                campaign (dict): database campaign config
                solution (dict): database solution config
            Return:
                (dict): current state config

        """
        state = {
            'should_update': False,
            'should_refresh_status': False
        }
        # get vendor campaign
        vendor_campaign = self.sagemaker.describe_endpoint(
            EndpointName=campaign.get('arn')
        )

        vendor_solution = self.sagemaker.describe_training_job(
            TrainingJobName=solution.get('arn')
        )

        vendor_solution_arn = self.get_vendor_solution_version_arn(
            vendor_solution=vendor_solution
        )

        state['should_update'] = self.should_update(
            vendor_campaign=vendor_campaign,
            vendor_solution=vendor_solution
        )

        if state['should_update']:
            state.update({
                'latest_solution_version_arn': vendor_solution_arn
            })

        else:
            # Check if the database status needs to be updated
            status = campaign.get('status', None)

            vendor_campaign_status = self.get_vendor_campaign_status(
                vendor_campaign=vendor_campaign
            )

            if vendor_campaign_status != status:
                state['should_refresh_status'] = True
                state['new_status'] = vendor_campaign_status

        return state

    def should_update(
            self,
            *,
            vendor_campaign: dict,
            vendor_solution: dict
    ) -> bool:
        """
            Check whether a campaign should be updated when all of the following are true

            args:
                vendor_campaign(dict): Campaign from Vendor
                vendor_solution (dict): solution from vendor

            returns:
                result (bool): Should update campaign

        """

        # get solution_version_arn from vendor campaign
        vendor_campaign_solution_version_arn = self.get_vendor_campaign_solution_version_arn(
            vendor_campaign=vendor_campaign
        )

        # get solution arn from vendor solution
        vendor_solution_version_arn = self.get_vendor_solution_version_arn(
            vendor_solution=vendor_solution
        )

        # get campaign status from vendor campaign
        vendor_campaign_status = self.get_vendor_campaign_status(
            vendor_campaign=vendor_campaign
        )

        # get solution status from vendor campaign
        latest_vendor_solution_version_status = self.get_vendor_solution_status(
            vendor_solution=vendor_solution
        )

        # Don't update dataset if its on the latest solution version
        if (
                vendor_solution_version_arn ==
                vendor_campaign_solution_version_arn
        ):
            return False

        if vendor_campaign_status in self.campaign_statuses['blocking']:
            return False

        # If the current campaign state == failed, update immediately
        if vendor_campaign_status in self.campaign_statuses['danger']:
            return True

        # Don't update campaign if the vendor solution version is not active
        if latest_vendor_solution_version_status not in self.solution_statuses['success']:
            return False

        return True

    def update_state(self, campaign: dict, solution: dict):
        """
            Run the update workflow for campaigns

            Args:
                campaign (dict): database campaign config
                solution (dict): database solution config
            Return:
                (dict): new campaign config

        """
        new_campaign = {
            'arn': None,
            'solution_version_arn': None,
            'status': None,
            'last_updated_at': None
        }

        # get vendor current campaign
        vendor_campaign = self.sagemaker.describe_endpoint(
            EndpointName=campaign.get('arn')
        )

        # get vendor current solution
        vendor_solution = self.sagemaker.describe_training_job(
            TrainingJobName=solution.get('arn')
        )

        # run vendor campaign update workflow
        response = self.sagemaker_update_campaign(
            EndpointName=vendor_campaign.get('EndpointName'),
            TrainingJobName=vendor_solution.get('TrainingJobName')
        )
        new_campaign['arn'] = response.get('EndpointName')
        new_campaign['solution_version_arn'] = vendor_solution.get('TrainingJobName')

        # get the current time as last updated at time
        current_time_at_update = datetime.strftime(
            datetime.now(),
            self.date_utils.get_mysql_date_format()
        )
        new_campaign.update({
            'last_updated_at': current_time_at_update
        })

        # set new campaign status as updating status
        new_campaign.update({
            'status': self.campaign_statuses['updating'][0]
        })

        # get next update time, this is not a required trigger here
        # deprecate this going forward
        next_update_time = new_campaign.get('next_update_time', None)
        if next_update_time is not None:
            new_campaign.update({
                'next_update_time': next_update_time
            })

        return new_campaign
