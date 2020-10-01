__copyright__ = "Copyright (c) 2020 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

from typing import Iterable, List

from .queryset.dunderkey import dunder_get
from .. import QuerySetReader, BaseRecursiveDriver

if False:
    from ...proto import jina_pb2


class SortQL(QuerySetReader, BaseRecursiveDriver):
    """Sorts the incoming of the documents by the value of a given field.
     It can also work in reverse mode

        Example::
        - !ReduceAllDriver
            with:
                traversal_paths: ['m']
        - !SortQL
            with:
                reverse: true
                field: 'score.value'
                traversal_paths: ['m']
        - !SliceQL
            with:
                start: 0
                end: 50
                granularity_range: [0, 0]
                adjacency_range: [0, 1]

        `SortQL` will ensure that only the documents are sorted by the score value before slicing the first top 50 documents
    """

    def __init__(self, field: str, reverse: bool = False, traversal_paths: List[str] = ['c'], *args, **kwargs):
        """
        :param field: the value of the field drives the sort of the iterable docs
        :param reverse: sort the value from big to small
        """

        super().__init__(traversal_paths=traversal_paths, *args, **kwargs)
        self._reverse = reverse
        self._field = field
        self.is_apply = False
        self._use_tree_traversal = True

    def _apply_all(self, docs: Iterable['jina_pb2.Document'], *args, **kwargs) -> None:
        docs.sort(key=lambda x: dunder_get(x, self.field), reverse=self.reverse)
