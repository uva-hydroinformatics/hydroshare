"""
This calls all preparation routines involved in creating SOLR records.
It is used to debug SOLR harvesting. If any of these routines fails on
any resource, all harvesting ceases. This has caused many bugs.
"""

from django.core.management.base import BaseCommand
from hs_core.models import BaseResource
from hs_core.search_indexes import BaseResourceIndex
from hs_core.hydroshare.utils import get_resource_by_shortkey
from pprint import pprint


def debug_harvest():
    ind = BaseResourceIndex()
    for obj in BaseResource.objects.all():
        res = get_resource_by_shortkey(obj.short_id, or_404=False)
        print ("TESTING RESOURCE {}".format(res.metadata.title.encode('ascii', 'ignore')))
        print('sample_medium')
        pprint(ind.prepare_sample_medium(res))
        print('creator')
        pprint(ind.prepare_creator(res))
        print('title')
        pprint(ind.prepare_title(res))
        print('abstract')
        pprint(ind.prepare_abstract(res))
        print('author_raw')
        pprint(ind.prepare_author_raw(res))
        print('author')
        pprint(ind.prepare_author(res))
        print('author_url')
        pprint(ind.prepare_author_url(res))
        print('creator')
        pprint(ind.prepare_creator(res))
        print('contributor')
        pprint(ind.prepare_contributor(res))
        print('subject')
        pprint(ind.prepare_subject(res))
        print('organization')
        pprint(ind.prepare_organization(res))
        print('publisher')
        pprint(ind.prepare_publisher(res))
        print('creator_email')
        pprint(ind.prepare_creator_email(res))
        print('availability')
        pprint(ind.prepare_availability(res))
        print('replaced')
        pprint(ind.prepare_replaced(res))
        print('coverage')
        pprint(ind.prepare_coverage(res))
        print('coverage_type')
        pprint(ind.prepare_coverage_type(res))
        print('east')
        pprint(ind.prepare_east(res))
        print('north')
        pprint(ind.prepare_north(res))
        print('northlimit')
        pprint(ind.prepare_northlimit(res))
        print('eastlimit')
        pprint(ind.prepare_eastlimit(res))
        print('southlimit')
        pprint(ind.prepare_southlimit(res))
        print('westlimit')
        pprint(ind.prepare_westlimit(res))
        print('start_date')
        pprint(ind.prepare_start_date(res))
        print('end_date')
        pprint(ind.prepare_end_date(res))
        print('format')
        pprint(ind.prepare_format(res))
        print('identifier')
        pprint(ind.prepare_identifier(res))
        print('language')
        pprint(ind.prepare_language(res))
        print('source')
        pprint(ind.prepare_source(res))
        print('relation')
        pprint(ind.prepare_relation(res))
        print('resource_type')
        pprint(ind.prepare_resource_type(res))
        print('comment')
        pprint(ind.prepare_comment(res))
        print('comments_count')
        pprint(ind.prepare_comments_count(res))
        print('owner_login')
        pprint(ind.prepare_owner_login(res))
        print('owner')
        pprint(ind.prepare_owner(res))
        print('owners_count')
        pprint(ind.prepare_owners_count(res))
        print('geometry_type')
        pprint(ind.prepare_geometry_type(res))
        print('field_name')
        pprint(ind.prepare_field_name(res))
        print('field_type')
        pprint(ind.prepare_field_type(res))
        print('field_type_code')
        pprint(ind.prepare_field_type_code(res))
        print('variable')
        pprint(ind.prepare_variable(res))
        print('variable_type')
        pprint(ind.prepare_variable_type(res))
        print('variable_shape')
        pprint(ind.prepare_variable_shape(res))
        print('variable_descriptive_name')
        pprint(ind.prepare_variable_descriptive_name(res))
        print('variable_speciation')
        pprint(ind.prepare_variable_speciation(res))
        print('site')
        pprint(ind.prepare_site(res))
        print('method')
        pprint(ind.prepare_method(res))
        print('quality_level')
        pprint(ind.prepare_quality_level(res))
        print('data_source')
        pprint(ind.prepare_data_source(res))
        print('sample_medium')
        pprint(ind.prepare_sample_medium(res))
        print('units')
        pprint(ind.prepare_units(res))
        print('units_type')
        pprint(ind.prepare_units_type(res))
        print('aggregation_statistics')
        pprint(ind.prepare_aggregation_statistics(res))
        print('absolute_url')
        pprint(ind.prepare_absolute_url(res))
        print('extra')
        pprint(ind.prepare_extra(res))


class Command(BaseCommand):
    help = "Print debugging information about logical files."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        debug_harvest()
