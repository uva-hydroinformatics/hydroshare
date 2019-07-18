import os

from django.test import TransactionTestCase
from django.contrib.auth.models import Group

from hs_core.testing import MockIRODSTestCaseMixin
from hs_core import hydroshare
from hs_core.models import ResourceFile
from hs_core.views.utils import move_or_rename_file_or_folder, remove_folder
from utils import CompositeResourceTestMixin
from hs_file_types.models import ModelInstanceLogicalFile 


class ModelInstanceTest(MockIRODSTestCaseMixin, TransactionTestCase,
                          CompositeResourceTestMixin):
    def setUp(self):
        super(ModelInstanceTest, self).setUp()
        self.group, _ = Group.objects.get_or_create(name='Hydroshare Author')
        self.user = hydroshare.create_account(
            'user1@nowhere.com',
            username='user1',
            first_name='Creator_FirstName',
            last_name='Creator_LastName',
            superuser=False,
            groups=[self.group]
        )

        self.res_title = "Test Model Instance Type"
        self.logical_file_type_name = "ModelInstanceLogicalFile"
        base_file_path = 'hs_file_types/tests/{}'
        self.generic_file_name = 'generic_file.txt'
        self.generic_file = base_file_path.format(self.generic_file_name)

    def test_create_model_instance_logical_file(self):
        """Test that we can create a model instance aggregation from a folder that contains one file """

        self.create_composite_resource()
        new_folder = 'model_instance_folder'
        ResourceFile.create_folder(self.composite_resource, new_folder)
        # add the the txt file to the resource at the above folder
        self.add_file_to_resource(file_to_add=self.generic_file, upload_folder=new_folder)
        # there should be one resource file
        self.assertEqual(self.composite_resource.files.all().count(), 1)
        res_file = self.composite_resource.files.first()
        # file has a folder
        self.assertEqual(res_file.file_folder, new_folder)
        # check that the resource file is not part of an aggregation
        self.assertEqual(res_file.has_logical_file, False)
        self.assertEqual(ModelInstanceLogicalFile.objects.count(), 0)
        # set folder to fileset logical file type (aggregation)
        ModelInstanceLogicalFile.set_file_type(self.composite_resource, self.user, folder_path=new_folder)
        res_file = self.composite_resource.files.first()
        # file has the same folder
        self.assertEqual(res_file.file_folder, new_folder)
        self.assertEqual(res_file.logical_file_type_name, self.logical_file_type_name)
        self.assertEqual(ModelInstanceLogicalFile.objects.count(), 1)
        # aggregation dataset name should be same as the folder name
        self.assertEqual(res_file.logical_file.dataset_name, new_folder)

        self.composite_resource.delete()

    def test_model_instance_metadata(self):
        """Test that we can add metadata to logical file """

        self.create_composite_resource()
        new_folder = 'model_instance_folder'
        ResourceFile.create_folder(self.composite_resource, new_folder)
        # add the the txt file to the resource at the above folder
        self.add_file_to_resource(file_to_add=self.generic_file, upload_folder=new_folder)
        res_file = self.composite_resource.files.first()
        self.assertEqual(ModelInstanceLogicalFile.objects.count(), 0)
        ModelInstanceLogicalFile.set_file_type(self.composite_resource, self.user, folder_path=new_folder)
        res_file = self.composite_resource.files.first()
        self.assertEqual(ModelInstanceLogicalFile.objects.count(), 1)
        self.assertEqual(res_file.logical_file_type_name, self.logical_file_type_name)

        logical_file = res_file.logical_file
        my_model_name = 'my model'
        my_model_url = 'http://www.google.com'
        logical_file.metadata.create_element('ModelOutput', includes_output=True)
        logical_file.metadata.create_element('ExecutedBy',
                                             model_name=my_model_name,
                                             model_url=my_model_url
                                             )
        self.assertEqual(logical_file.metadata.model_output.includes_output, True)
        self.assertEqual(logical_file.metadata.executed_by.model_name, my_model_name)
        self.assertEqual(logical_file.metadata.executed_by.model_url, my_model_url)

        self.composite_resource.delete()
