
import os

from django.test import TransactionTestCase
from django.contrib.auth.models import Group

from hs_core.testing import MockIRODSTestCaseMixin
from hs_core import hydroshare
from hs_core.models import ResourceFile
from hs_core.views.utils import move_or_rename_file_or_folder, remove_folder
from utils import CompositeResourceTestMixin
from hs_file_types.models import ModelProgramLogicalFile 


class ModelProgramTest(MockIRODSTestCaseMixin, TransactionTestCase,
                          CompositeResourceTestMixin):
    def setUp(self):
        super(ModelProgramTest, self).setUp()
        self.group, _ = Group.objects.get_or_create(name='Hydroshare Author')
        self.user = hydroshare.create_account(
            'user1@nowhere.com',
            username='user1',
            first_name='Creator_FirstName',
            last_name='Creator_LastName',
            superuser=False,
            groups=[self.group]
        )

        self.res_title = "Test Model Program Type"
        self.logical_file_type_name = "ModelProgramLogicalFile"
        base_file_path = 'hs_file_types/tests/{}'
        self.generic_file_name = 'generic_file.txt'
        self.generic_file = base_file_path.format(self.generic_file_name)

    def test_create_model_program_logical_file(self):
        """Test that we can create a model program aggregation from a folder that contains one file """

        self.create_composite_resource()
        new_folder = 'model_program_folder'
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
        self.assertEqual(ModelProgramLogicalFile.objects.count(), 0)
        # set folder to fileset logical file type (aggregation)
        ModelProgramLogicalFile.set_file_type(self.composite_resource, self.user, folder_path=new_folder)
        res_file = self.composite_resource.files.first()
        # file has the same folder
        self.assertEqual(res_file.file_folder, new_folder)
        self.assertEqual(res_file.logical_file_type_name, self.logical_file_type_name)
        self.assertEqual(ModelProgramLogicalFile.objects.count(), 1)
        # aggregation dataset name should be same as the folder name
        self.assertEqual(res_file.logical_file.dataset_name, new_folder)

        self.composite_resource.delete()

    def test_model_program_metadata(self):
        """Test that we can add metadata to logical file """

        self.create_composite_resource()
        new_folder = 'model_program_folder'
        ResourceFile.create_folder(self.composite_resource, new_folder)
        # add the the txt file to the resource at the above folder
        self.add_file_to_resource(file_to_add=self.generic_file, upload_folder=new_folder)
        res_file = self.composite_resource.files.first()
        self.assertEqual(ModelProgramLogicalFile.objects.count(), 0)
        ModelProgramLogicalFile.set_file_type(self.composite_resource, self.user, folder_path=new_folder)
        res_file = self.composite_resource.files.first()
        self.assertEqual(ModelProgramLogicalFile.objects.count(), 1)
        self.assertEqual(res_file.logical_file_type_name, self.logical_file_type_name)
        logical_file = res_file.logical_file

        ver = '1'
        lang = 'c++'
        os = 'windows'
        date = '2015-11-21 00:00'
        site = 'http://www.google.com'
        repo = 'http://github.com/my_sweet_repo'
        cont_repo = 'http://dockerhub.com/my_sweet_repo'
        notes = 'notes.txt'
        docs = 'doc.txt'
        software = 'my_software.zip'
        engine = 'my_engine.exe'
        logical_file.metadata.create_element('MpMetadata',
                                             modelVersion=ver,
                                             modelProgramLanguage=lang,
                                             modelOperatingSystem=os,
                                             modelReleaseDate=date,
                                             modelWebsite=site,
                                             modelCodeRepository=repo,
                                             modelContainerRepository=cont_repo,
                                             modelReleaseNotes=notes,
                                             modelDocumentation=docs,
                                             modelSoftware=software,
                                             modelEngine=engine
                                             )
        self.assertEqual(logical_file.metadata.program.modelVersion, ver)
        self.assertEqual(logical_file.metadata.program.modelProgramLanguage, lang)
        self.assertEqual(logical_file.metadata.program.modelOperatingSystem, os)
        self.assertEqual(logical_file.metadata.program.modelReleaseDate.strftime('%Y-%m-%d %H:%M'),
                         date)
        self.assertEqual(logical_file.metadata.program.modelWebsite, site)
        self.assertEqual(logical_file.metadata.program.modelCodeRepository, repo)
        self.assertEqual(logical_file.metadata.program.modelContainerRepository, cont_repo)
        self.assertEqual(logical_file.metadata.program.modelReleaseNotes, notes)
        self.assertEqual(logical_file.metadata.program.modelDocumentation, docs)
        self.assertEqual(logical_file.metadata.program.modelSoftware, software)
        self.assertEqual(logical_file.metadata.program.modelEngine, engine)

        self.composite_resource.delete()

