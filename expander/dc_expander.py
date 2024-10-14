import uuid

from owl_loader import RdfClass
from util.rdf_const import *
from util.string import from_humps
from vo.Container import Container
from vo.Content import Content
from vo.DataComponent import DataComponent
from vo.DataComponentWrapper import DataComponentWrapper
from vo.Heading import Heading
from vo.TextContent import TextContent


def convert_rdf_class(rdf_class: RdfClass, is_root: bool) -> DataComponent:
    i = 0
    contains = []

    # ------------------------------------------------------------------------------------------------------------------
    # DATA TYPES
    # ------------------------------------------------------------------------------------------------------------------
    data_types = list(rdf_class.data_types)
    # 1. Title
    titles = [dt for dt in data_types if dt.name == DC_TERMS_TITLE]
    if len(titles) == 1:
        contains.append(Heading(
            name=create_unique_name("Heading"),
            order=i,
            is_block=True,
            contains=[
                Content(
                    name=create_unique_name("Content"),
                    order=0,
                    predicate=DC_TERMS_TITLE
                )
            ]
        ))
        i += 1
        data_types.remove(titles[0])
    # 2. Description
    descriptions = [dt for dt in data_types if dt.name == DC_TERMS_DESCRIPTION]
    if len(descriptions) == 1:
        contains.append(
            Content(
                name=create_unique_name("Content"),
                order=i,
                predicate=DC_TERMS_DESCRIPTION
            )
        )
        i += 1
        data_types.remove(descriptions[0])
    # 3. Start, StartDate, Issued
    dates = [dt for dt in data_types if
             dt.name == DCSO_START or dt.name == DCSO_START_DATE or dt.name == DC_TERMS_ISSUED]
    for date in dates:
        contains.append(Container(
            name=create_unique_name("Container"),
            order=i,
            is_block=True,
            contains=[
                Content(
                    name=create_unique_name("Content"),
                    order=0,
                    contentContent=TextContent(
                        name=create_unique_name("TextContent"),
                        order=0,
                        value=create_title(date.name)
                    )
                ),
                Content(
                    name=create_unique_name("Content"),
                    order=1,
                    predicate=date.name,
                    content="Date"
                )
            ]))
        i += 1
        data_types.remove(date)
    # 4. Start, StartDate, Issued
    dates = [dt for dt in data_types if dt.name == DCSO_UNTIL or dt.name == DCSO_END]
    for date in dates:
        contains.append(Container(
            name=create_unique_name("Container"),
            order=i,
            is_block=True,
            contains=[
                Content(
                    name=create_unique_name("Content"),
                    order=0,
                    contentContent=TextContent(
                        name=create_unique_name("TextContent"),
                        order=0,
                        value=create_title(date.name)
                    )
                ),
                Content(
                    name=create_unique_name("Content"),
                    order=1,
                    predicate=date.name,
                    content="Date"
                )
            ]))
        i += 1
        data_types.remove(date)
    # 5. Other data types
    for data_type in data_types:
        content = None
        if data_type.name == FOAF_MBOX:
            content = "Email"
        elif data_type.name == DCSO_CREATED:
            content = "DateTime"
        elif data_type.name == DCAT_ACCESS_URL \
                or data_type.name == DCAT_DOWNLOAD_URL:
            content = "Url"
        contains.append(Container(
            name=create_unique_name("Container"),
            order=i,
            is_block=True,
            contains=[
                Content(
                    name=create_unique_name("Content"),
                    order=0,
                    predicate=data_type.name,
                    content=content
                )
            ]))
        i += 1

    # ------------------------------------------------------------------------------------------------------------------
    # OBJECTS
    # ------------------------------------------------------------------------------------------------------------------
    for object in rdf_class.objects:
        contains.append(DataComponentWrapper(
            name=create_unique_name("DataComponentWrapper"),
            order=i,
            predicate=object.name,
            data_component=convert_rdf_class(object.rdf_class, is_root=False)
        ))
        i += 1

    name = "Root" if is_root else create_unique_name("DataComponent")
    class_name = "Root" if is_root else rdf_class.name.split("#")[1]
    return DataComponent(
        name=name,
        class_name=class_name,
        content=Container(
            name=create_unique_name("Container"),
            order=0,
            is_block=True,
            contains=contains
        )
    )


def create_title(value: str) -> str:
    if '#' in value:
        return ' '.join(from_humps(value.split("#")[1])).capitalize() + ': '
    else:
        return ' '.join(from_humps(value.split("/")[-1])).capitalize() + ': '


def create_unique_name(type):
    return f'{type}_{uuid.uuid4().__str__().replace("-", "")}'
