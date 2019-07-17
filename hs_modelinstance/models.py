from lxml import etree

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models, transaction
from django.core.exceptions import ValidationError

from mezzanine.pages.page_processors import processor_for

from hs_core.models import BaseResource, ResourceManager, resource_processor, CoreMetaData, AbstractMetaDataElement
from hs_core.hydroshare import utils

from hs_model_program.models import ModelProgramResource


# extended metadata elements for Model Instance resource type
class ModelOutput(AbstractMetaDataElement):
    term = 'ModelOutput'
    includes_output = models.BooleanField(default=False)

    def __unicode__(self):
        return self.includes_output

    class Meta:
        # ModelOutput element is not repeatable
        unique_together = ("content_type", "object_id")

    @property
    def includesModelOutput(self):
        if self.includes_output:
            return "Yes"
        else:
            return "No"


class ExecutedBy(AbstractMetaDataElement):
    term = 'ExecutedBY'
    # model_name: the id of the model program used for execution
    model_name = models.CharField(max_length=500, default=None)
    model_url = models.URLField(max_length=500, default=None)

    def __unicode__(self):
        return self.model_name

    class Meta:
        # ExecutedBy element is not repeatable
        unique_together = ("content_type", "object_id")


# Model Instance Resource type
class ModelInstanceResource(BaseResource):
    objects = ResourceManager("ModelInstanceResource")

    discovery_content_type = 'Model Instance'  # used during discovery

    class Meta:
        verbose_name = 'Model Instance Resource'
        proxy = True

    @classmethod
    def get_metadata_class(cls):
        return ModelInstanceMetaData

processor_for(ModelInstanceResource)(resource_processor)

class ModelInstanceMetaDataMixin(CoreMetaData):
    _model_output = GenericRelation(ModelOutput)
    _executed_by = GenericRelation(ExecutedBy)

    class Meta:
        abstract = True

    @property
    def model_output(self):
        return self._model_output.all().first()

    @property
    def executed_by(self):
        return self._executed_by.all().first()

    @classmethod
    def get_supported_element_names(cls):
        # get the names of all core metadata elements
        elements = super(ModelInstanceMetaData, cls).get_supported_element_names()
        # add the name of any additional element to the list
        elements.append('ModelOutput')
        elements.append('ExecutedBy')
        return elements

    def has_all_required_elements(self):
        if self.get_required_missing_elements():
            return False
        return True

    def get_required_missing_elements(self):  # show missing required meta
        missing_required_elements = super(GeographicFeatureMetaDataMixin, self). \
            get_required_missing_elements()
        if not self._executed_by.model_name:
            missing_required_elements.append('Executed By Model Name')

        return missing_required_elements

# metadata container class
class ModelInstanceMetaData(CoreMetaData):

    @property
    def resource(self):
        return ModelInstanceResource.objects.filter(object_id=self.id).first()


    @property
    def serializer(self):
        """Return an instance of rest_framework Serializer for self """
        from serializers import ModelInstanceMetaDataSerializer
        return ModelInstanceMetaDataSerializer(self)

    @classmethod
    def parse_for_bulk_update(cls, metadata, parsed_metadata):
        """Overriding the base class method"""

        CoreMetaData.parse_for_bulk_update(metadata, parsed_metadata)
        keys_to_update = metadata.keys()
        if 'modeloutput' in keys_to_update:
            parsed_metadata.append({"modeloutput": metadata.pop('modeloutput')})

        if 'executedby' in keys_to_update:
            parsed_metadata.append({"executedby": metadata.pop('executedby')})

    def update(self, metadata, user):
        # overriding the base class update method for bulk update of metadata
        from forms import ModelOutputValidationForm, ExecutedByValidationForm

        super(ModelInstanceMetaData, self).update(metadata, user)
        attribute_mappings = {'modeloutput': 'model_output', 'executedby': 'executed_by'}
        with transaction.atomic():
            # update/create non-repeatable element
            for element_name in attribute_mappings.keys():
                for dict_item in metadata:
                    if element_name in dict_item:
                        if element_name == 'modeloutput':
                            validation_form = ModelOutputValidationForm(dict_item[element_name])
                        else:
                            validation_form = ExecutedByValidationForm(dict_item[element_name])
                        if not validation_form.is_valid():
                            err_string = self.get_form_errors_as_string(validation_form)
                            raise ValidationError(err_string)
                        element_property_name = attribute_mappings[element_name]
                        self.update_non_repeatable_element(element_name, metadata,
                                                           element_property_name)

    def get_xml(self, pretty_print=True, include_format_elements=True):
        # get the xml string representation of the core metadata elements
        print "do I go here??"
        xml_string = super(ModelInstanceMetaData, self).get_xml(pretty_print=pretty_print)

        # create an etree xml object
        RDF_ROOT = etree.fromstring(xml_string)

        # get root 'Description' element that contains all other elements
        container = RDF_ROOT.find('rdf:Description', namespaces=self.NAMESPACES)

        if self.model_output:
            modelOutputFields = ['includesModelOutput']
            self.add_metadata_element_to_xml(container,self.model_output,modelOutputFields)

        if self.executed_by:
            executed_by = self.executed_by
        else:
            executed_by = ExecutedBy()

        executedByFields = ['modelProgramName','modelProgramIdentifier']
        self.add_metadata_element_to_xml(container,executed_by,executedByFields)

        return etree.tostring(RDF_ROOT, pretty_print=pretty_print)

    def delete_all_elements(self):
        super(ModelInstanceMetaData, self).delete_all_elements()
        self._model_output.all().delete()
        self._executed_by.all().delete()

import receivers
