__author__ = 'drew'

from django import forms
from crispy_forms.layout import Layout, Field, HTML
from hs_core.forms import BaseFormHelper

class OriginalCoverageFormHelper(BaseFormHelper):
    def __init__(self, allow_edit=True, res_short_id=None, element_id=None, element_name=None,  *args, **kwargs):

        # the order in which the model fields are listed for the FieldSet is the order these fields will be displayed
        field_width = 'form-control input-sm'
        layout = Layout(
                        Field('projection_name', css_class=field_width),
                        Field('datum', css_class=field_width),
                        Field('unit', css_class=field_width),
                        Field('projection_string', css_class=field_width),
                        Field('northlimit', css_class=field_width),
                        Field('eastlimit', css_class=field_width),
                        Field('southlimit', css_class=field_width),
                        Field('westlimit', css_class=field_width),
                       )

        super(OriginalCoverageFormHelper, self).__init__(allow_edit, res_short_id, element_id, element_name, layout,
                                                         element_name_label='Spatial Reference', *args, **kwargs)

class OriginalCoverageForm(forms.Form):
    projection_string = forms.CharField(required=False, label='Coordinate String',
                                        widget=forms.Textarea())
    projection_name = forms.CharField(max_length=256, required=False, label='Coordinate Reference System')
    datum = forms.CharField(max_length=256, required=False, label='Datum')
    unit = forms.CharField(max_length=256, required=False, label='Unit')

    northlimit = forms.FloatField(label='North Extent', widget=forms.TextInput())
    eastlimit = forms.FloatField(label='East Extent', widget=forms.TextInput())
    southlimit = forms.FloatField(label='South Extent', widget=forms.TextInput())
    westlimit = forms.FloatField(label='West Extent', widget=forms.TextInput())

    def __init__(self, allow_edit=True, res_short_id=None, element_id=None, *args, **kwargs):
        super(OriginalCoverageForm, self).__init__(*args, **kwargs)
        self.helper = OriginalCoverageFormHelper(allow_edit, res_short_id, element_id, element_name='OriginalCoverage')
        self.delete_modal_form = None
        self.number = 0
        self.allow_edit = allow_edit
        self.errors.clear()

        if not allow_edit:
            for field in self.fields.values():
                field.widget.attrs['readonly'] = True
                field.widget.attrs['style'] = "background-color:white;"

class OriginalCoverageValidationForm(forms.Form):
    northlimit = forms.FloatField(required=True)
    eastlimit = forms.FloatField(required=True)
    southlimit = forms.FloatField(required=True)
    westlimit = forms.FloatField(required=True)
    projection_string = forms.CharField(required=False)
    projection_name = forms.CharField(max_length=256, required=False)
    datum = forms.CharField(max_length=256, required=False)
    unit = forms.CharField(max_length=256, required=False)


class GeometryInformationFormHelper(BaseFormHelper):
    def __init__(self, allow_edit=True, res_short_id=None, element_id=None, element_name=None,  *args, **kwargs):

        # the order in which the model fields are listed for the FieldSet is the order these fields will be displayed
        field_width = 'form-control input-sm'
        layout = Layout(
                        Field('geometryType', css_class=field_width),
                        Field('featureCount', css_class=field_width),
                       )

        super(GeometryInformationFormHelper, self).__init__(allow_edit, res_short_id, element_id, element_name,
                                                            layout, element_name_label='Geometry Information',
                                                            *args, **kwargs)

class GeometryInformationForm(forms.Form):
    geometryType = forms.CharField(max_length=128, required=True, label='Geometry Type')
    featureCount = forms.IntegerField(label='Feature Count', required=True, widget=forms.TextInput())

    def __init__(self, allow_edit=True, res_short_id=None, element_id=None, *args, **kwargs):
        super(GeometryInformationForm, self).__init__(*args, **kwargs)
        self.helper = GeometryInformationFormHelper(allow_edit, res_short_id, element_id,\
                                                    element_name='GeometryInformation')
        self.delete_modal_form = None
        self.number = 0
        self.allow_edit = allow_edit
        self.errors.clear()

        if not allow_edit:
            for field in self.fields.values():
                field.widget.attrs['readonly'] = True
                field.widget.attrs['style'] = "background-color:white;"

class GeometryInformationValidationForm(forms.Form):
    featureCount = forms.IntegerField(required=True)
    geometryType = forms.CharField(max_length=128, required=True)

class FieldInformationValidationForm(forms.Form):
    fieldName = forms.CharField(required=True, max_length=128)
    fieldType = forms.CharField(required=True, max_length=128)
    fieldTypeCode = forms.CharField(required=False, max_length=50)
    fieldWidth = forms.DecimalField(required=False)
    fieldPrecision = forms.DecimalField(required=False)