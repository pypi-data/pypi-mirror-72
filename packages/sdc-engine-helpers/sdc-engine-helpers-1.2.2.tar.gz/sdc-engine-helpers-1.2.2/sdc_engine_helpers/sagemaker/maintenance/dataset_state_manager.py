"""
    Dataset state manager module
        - state managers have knowledge of state transition and meaning
        - state manager is called to check state
        - state manager is called to transition state
        - state manager only sends back True/False. Do something or don't.

        may want to:
        - add validation of complex types: Url, etc https://validators.readthedocs.io/en/latest/
"""
import io
import json
from urllib.parse import urlparse
from datetime import datetime
import sdc_helpers.utils as utils
import boto3
from sdc_engine_helpers.date_utils import DateUtils

# pylint: disable=too-few-public-methods
class DatasetStateManager:
    """
        Given a database dataset object,

        1. get_state
            - check whether dataset should be updated by
                call vendor API's to check if campaign solution
                version differs from dataset solution version
            OR
            - check if the dataset status in the database needs to be refreshed.
        2. update_state
            - call vendor API's to execute update workflow for dataset
            - update status of dataset in database

    """
    date_utils = DateUtils()
    # vendor
    vendor_campaign_arn_path = 'EndpointName'
    vendor_campaign_status_path = 'EndpointStatus'
    # input data key in TrainingJob
    vendor_campaign_solution_arn_path = 'ProductionVariants.0.VariantName'

    campaign_statuses = {
        'running':['Creating', 'Updating', 'SystemUpdating', 'Deleting'],
        'failed':['Failed', 'RollingBack'],
        'danger':['Failed'],
        'blocking':[
            'Creating',
            'Updating',
            'SystemUpdating',
            'Deleting',
            'Failed',
            'RollingBack'],
        'stopped':['OutOfService'],
        'active':['InService']
    }

    solution_statuses = {
        'blocking':['InProgress', 'Stopping', 'Failed', 'Stopped'],
        'success':['Completed']
    }

    dataset_statuses = {
        'active': ['Active'],
        'blocking': ['Updating']
    }

    def __init__(self):
        self.sagemaker = boto3.client('sagemaker')
        self.s3_client = boto3.client('s3')

    @staticmethod
    def get_vendor_solution_dataset_identifier(
            *,
            vendor_solution: dict,
            dataset_label: str,
            filetype: str
        ) -> str:
        """
            Get a Sagemaker Training job input dataset by channel name

            args:
                vendor_solution (dict): Solution from Personalize
                dataset_label (str): dataset label as stored in db

            returns:
                status (str): Sagemaker solution version status

        """
        input_configs = vendor_solution.get("InputDataConfig")
        if input_configs is not None:
            for d_configs in input_configs:
                print(d_configs)
                channel_name = d_configs.get("ChannelName")

                if channel_name is None:
                    raise Exception("ChannelName must be provided by vendor")

                print(dataset_label)
                if channel_name == dataset_label:
                    s3_folder_path = utils.dict_query(
                        dictionary=d_configs,
                        path='DataSource.S3DataSource.S3Uri'
                    )
                    return "{}/{}.{}".format(
                        s3_folder_path,
                        dataset_label,
                        filetype
                    )

        raise ValueError("InputDataConfig is missing, vendor should provide this.")

    @staticmethod
    def parse_s3_url(url: str):
        """
            Parse S3URL to find bucket name and filepath

            args:
                url (str): string s3:// url
            return:
                (bucket-name (str), s3 filepath (str))
        """
        url_obj = urlparse(url, allow_fragments=False)

        return url_obj.netloc, url_obj.path

    def upload_lookups(self, s3_url: str):
        """Upload dataset from s3"""

        # parse s3 url -> bucket, file_path
        bucket, file_path = self.parse_s3_url(s3_url)
        # load data from s3 as byte steam
        data_stream = io.BytesIO()
        self.s3_client.download_fileobj(bucket,
                                        file_path,
                                        data_stream)
        data_stream.seek(0)
        return json.loads(data_stream.read().decode("UTF-8"))

    def get_vendor_campaign_solution_version_arn(self, vendor_campaign: dict):
        """
            Get vendor campaign solution version status

            args:
                vendor_campaign (dict): Solution from vendor campaign

            returns:
                status (str): vendor solution version status

        """

        return utils.dict_query(
            dictionary=vendor_campaign,
            path=self.vendor_campaign_solution_arn_path
        )

    def get_vendor_campaign_status(self, vendor_campaign: dict):
        """
            Get vendor campaign solution version status

            args:
                vendor_campaign (dict): Solution from vendor campaign

            returns:
                status (str): vendor solution version status

        """

        return utils.dict_query(
            dictionary=vendor_campaign,
            path=self.vendor_campaign_status_path
        )

    def get_state(
            self, *,
            dataset: dict,
            campaign: dict):
        """
            Get dataset state

            Args:
                dataset (dict): database dataset config
                campaign (dict): database campaign config
            Return:
                (dict): current state config
        """
        state = {
            'should_update': False
        }

        # get current campaign from vendor
        vendor_campaign = self.sagemaker.describe_endpoint(
            EndpointName=campaign.get('arn')
        )

        # check if should update
        state['should_update'] = self.should_update(
            dataset=dataset,
            vendor_campaign=vendor_campaign
        )

        if state['should_update']:
            # set a new version status as InProgress
            state.update(
                {
                    'new_version_status': 'Updating'
                }
            )

        return state

    def update_state(
            self, *,
            dataset: dict,
            campaign: dict
        ):
        """
            This is where jobs to create datasets are run

            Args:
                dataset (dict): database dataset config
                campaign (dict): database campaign config
            Return:
                (dict): new dataset
        """

        new_dataset = {
            'data': None,
            'identifier': None,
            'solution_version_arn': None,
            'last_updated_at': None,
            'last_status': None
        }

        # get vendor solution
        vendor_campaign = self.sagemaker.describe_endpoint(
            EndpointName=campaign.get('arn')
        )

        # get vendor campaign
        latest_vendor_solution_version_arn = self.get_vendor_campaign_solution_version_arn(
            vendor_campaign
        )

        vendor_solution = self.sagemaker.describe_training_job(
            TrainingJobName=latest_vendor_solution_version_arn
        )

        # update solution arn
        new_dataset.update({
            'solution_version_arn': latest_vendor_solution_version_arn
        })

        # update identifier
        new_dataset.update({
            'identifier': self.get_vendor_solution_dataset_identifier(
                vendor_solution=vendor_solution,
                dataset_label=dataset['label'],
                filetype=dataset['datatype']
            )
        })

        if dataset.get('should_store'):
            # update data
            identifier = new_dataset.get('identifier', None)
            # get dataset from reference
            if isinstance(identifier, str):
                new_dataset.update({
                    'data':self.upload_lookups(
                        s3_url=identifier)
                })

        # date
        new_dataset.update({
            'last_updated_at': datetime.strftime(
                datetime.now(),
                self.date_utils.get_mysql_date_format()
                )
        })

        # update status
        new_dataset.update({
            'last_status': 'Active'
        })

        return new_dataset

    def should_update(
            self,
            *,
            dataset: dict,
            vendor_campaign: dict
    ) -> bool:
        """Check if dataset should update"""
        # (look at campaign state manager)
        latest_vendor_campaign_solution_version_arn = self.get_vendor_campaign_solution_version_arn(
            vendor_campaign
        )

        latest_vendor_campaign_status = self.get_vendor_campaign_status(
            vendor_campaign
        )

        # Don't update dataset if its on the latest solution version
        if (
                dataset.get('solution_version_arn') ==
                latest_vendor_campaign_solution_version_arn
        ):
            return False

        if latest_vendor_campaign_status not in self.campaign_statuses['active']:
            return False

        if dataset.get('last_status') not in self.dataset_statuses['active']:
            return False

        return True
