#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from io import StringIO
from collections import OrderedDict

from tcflib.service import ExportingWorker, run_as_cli


class CSVExporter(ExportingWorker):

    def export(self):

        columns = OrderedDict()
        columns['tokenID'] = [token.id for token in self.corpus.tokens]
        columns['token'] = [token.text for token in self.corpus.tokens]
        if hasattr(self.corpus, 'postags'):
            columns['POStag'] = [token.tag for token in self.corpus.tokens]
        if hasattr(self.corpus, 'lemmas'):
            columns['lemma'] = [token.lemma for token in self.corpus.tokens]
        if hasattr(self.corpus, 'wsd'):
            columns['wordsenses'] = [', '.join(token.wordsenses)
                                     for token in self.corpus.tokens]
        if hasattr(self.corpus, 'namedentities'):
            entities = []
            for token in self.corpus.tokens:
                if not token.entity:
                    entities.append('')
                elif token == token.entity.tokens[0]:
                    entities.append('B-{}'.format(token.entity.class_))
                else:
                    entities.append('I-{}'.format(token.entity.class_))
            columns['NamedEntity'] = entities
        # Write to CSV
        with StringIO(newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(list(columns.keys()))
            for row in zip(*columns.values()):
                writer.writerow(row)
            outstring = csvfile.getvalue()
        return outstring.encode('utf-8')

if __name__ == '__main__':
    run_as_cli(CSVExporter)