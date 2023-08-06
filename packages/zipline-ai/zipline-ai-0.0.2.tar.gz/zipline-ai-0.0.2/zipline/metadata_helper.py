import zipline.schema.thrift.ttypes as ttypes
from typing import List, Dict, Union


def get_underlying_source(source: ttypes.Source):
    return source.entities if source.entities else source.events


def construct_dependencies(table: str, query: ttypes.Query) -> List[Dict[str, Union[int, str]]]:
    date_part = query.partitionColumn
    add_parts = query.additionalPartitions

    # TODO: we are leaking some airflow-isms here - IMO this file belongs to airflow code purely
    # But, if we also consider Open-Sourcing airflow code, it is not a problem.
    ds_string = "{{ ds }}"
    if query.partitionLag and query.partitionLag > 0:
        ds_string = f"{{{{ macros.ds_add(ds, -{query.partitionLag}) }}}}"

    add_part_list = add_parts.split("/") if add_parts else []
    if add_part_list:
        result = [{
            # = sign is not allowed in the name
            "name": f"wait_for_{table}_{part.replace('=', '_') + '_'}{date_part}",
            "spec": f"{table}/{date_part}={ds_string}/{part}",
            "start": query.startPartition,
            "end": query.endPartition
        } for part in add_part_list]
    else:
        result = [{
            "name": f"wait_for_{table}_{date_part}",
            "spec": f"{table}/{date_part}={ds_string}",
            "start": query.startPartition,
            "end": query.endPartition
        }]
    return result


def get_dependencies(source: ttypes.Source) -> List[Dict]:
    inner_source = get_underlying_source(source)
    query = inner_source.query
    base_table = source.entities.snapshotTable if source.entities else source.events.table
    dependencies = construct_dependencies(base_table, query)
    if source.entities and source.entities.mutationTable:
        dependencies += construct_dependencies(source.entities.mutationTable, query)
    return dependencies
