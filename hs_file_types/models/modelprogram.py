import os
import logging

from django.db import models

from hs_core.models import ResourceFile, CoreMetaData
from base import AbstractLogicalFile, AbstractFileMetaData

from hs_model_program.models import ModelProgramMetaDataMixin
from lxml import etree

class ModelProgramFileMetadata(ModelProgramMetaDataMixin, AbstractFileMetaData):
    model_app_label = 'hs_model_program'

    def get_metadata_elements(self):
        elements = super(ModelProgramFileMetadata, self).get_metadata_elements()
        elements += [self.program]
        return elements

    @classmethod
    def get_metadata_model_classes(cls):
        metadata_model_classes = super(ModelProgramFileMetadata, cls).get_metadata_model_classes()
        metadata_model_classes['program'] = MpMetadata
        return metadata_model_classes

    def get_html(self):
        pass

    def get_html_forms(self, datatset_name_form=True):
        pass 

    @classmethod
    def validate_element_data(cls, request, element_name):
        pass

    def get_xml(self, pretty_print=True):
        """Generates ORI+RDF xml for this aggregation metadata"""

        # get the xml root element and the xml element to which contains all other elements
        RDF_ROOT, container_to_add_to = super(ModelProgramFileMetadata, self)._get_xml_containers()
        if self.program:
            self.program.add_to_xml_container(container_to_add_to)

        return CoreMetaData.XML_HEADER + '\n' + etree.tostring(RDF_ROOT, encoding='UTF-8',
                                                               pretty_print=pretty_print)


class ModelProgramLogicalFile(AbstractLogicalFile):
    # In essence, I copied an pasted the ModelInstanceLogicalFile and just changed
    # anything that said "model instance" to "model program"
    metadata = models.OneToOneField(ModelProgramFileMetadata,
                                    related_name="logical_file")
    # folder path relative to {resource_id}/data/contents/ that represents this aggregation
    data_type = "ModelProgram"

    @classmethod
    def create(cls, resource):
        # this custom method MUST be used to create an instance of this class
        mp_metadata = ModelProgramFileMetadata.objects.create(keywords=[])
        # Note we are not creating the logical file record in DB at this point
        # the caller must save this to DB
        return cls(metadata=mp_metadata, resource=resource)

    @classmethod
    def get_primary_resouce_file(cls, resource_files):
        """Gets any one resource file from the list of files *resource_files* """

        return resource_files[0] if resource_files else None
    @staticmethod
    def get_aggregation_display_name():
        return 'Model Program: One or more files that make up a model program'

    @staticmethod
    def get_aggregation_type_name():
        return "ModelProgramAggregation"

    # used in discovery faceting to aggregate native and composite content types
    @staticmethod
    def get_discovery_content_type():
        """Return a human-readable content type for discovery.
        This must agree between Composite Types and native types (there is no equivalent native type
        for File Set).
        """
        return "Model Program"

    @classmethod
    def validate_element_data(cls, request, element_name):
        pass

    @classmethod
    def check_files_for_aggregation_type(cls, files):
        """Checks if the specified files can be used to set this aggregation type
        :param  files: a list of ResourceFile objects

        :return If the files meet the requirements of this aggregation type, then returns this
        aggregation class name, otherwise empty string.
        """
        if len(files) == 0:
            # no files
            return ""

        return cls.__name__

    @classmethod
    def set_file_type(cls, resource, user, file_id=None, folder_path=None):
        """Makes all physical files that are in a folder (*folder_path*) part of a file set
        aggregation type.
        Note: parameter file_id is ignored here and a value for folder_path is required
        """

        log = logging.getLogger()
        if folder_path is None:
            raise ValueError("Must specify folder to be set as a file set aggregation type")

        _, folder_path = cls._validate_set_file_type_inputs(resource, file_id, folder_path)

        folder_name = folder_path
        if '/' in folder_path:
            folder_name = os.path.basename(folder_path)

        logical_file = cls.initialize(folder_name, resource)
        logical_file.folder = folder_path
        # logical file record gets created in DB
        logical_file.save()
        # make all the files in the selected folder as part of the aggregation
        logical_file.add_resource_files_in_folder(resource, folder_path)
        logical_file.create_aggregation_xml_documents()
        log.info("File set aggregation was created for folder:{}.".format(folder_path))