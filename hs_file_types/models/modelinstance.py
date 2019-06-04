import os
import logging

from django.db import models

from hs_core.models import ResourceFile
from base import AbstractLogicalFile
from fileset import FileSetMetaData, FileSetLogicalFile


class ModelInstanceFileMetadata(FileSetMetaData):
    pass


class ModelInstanceLogicalFile(FileSetLogicalFile):
    # I copied an pasted the rest GenericLogicalFile and just changed anything
    # that said "generic" to "model instance"
    metadata = models.OneToOneField(ModelInstanceFileMetadata)
    # folder path relative to {resource_id}/data/contents/ that represents this aggregation
    data_type = "ModelInstance"

    @classmethod
    def create(cls, resource):
        # this custom method MUST be used to create an instance of this class
        mi_metadata = ModelInstanceFileMetadata.objects.create(keywords=[])
        # Note we are not creating the logical file record in DB at this point
        # the caller must save this to DB
        return cls(metadata=mi_metadata, resource=resource)

    @staticmethod
    def get_aggregation_display_name():
        return 'Model Instance: One or more files that make up a model instance'

    @staticmethod
    def get_aggregation_type_name():
        return "ModelInstanceAggregation"

    # used in discovery faceting to aggregate native and composite content types
    @staticmethod
    def get_discovery_content_type():
        """Return a human-readable content type for discovery.
        This must agree between Composite Types and native types (there is no equivalent native type
        for File Set).
        """
        return "Model Instance"

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
        log.info("Fie set aggregation was created for folder:{}.".format(folder_path))


