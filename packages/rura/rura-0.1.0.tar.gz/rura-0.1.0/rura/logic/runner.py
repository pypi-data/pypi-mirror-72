from rura.logic.class_def import ClassDef
from rura.logic.dataset import DatasetMaker
from rura.logic.model import ModelExecute
from rura.logic.sources import Sources
from rura.logic.transform import Transformer
from rura.utils.paths import PROJECT, DATA_PROCESSED, RESULTS
from ruamel.yaml import YAML
import warnings
import logging
import shutil
import os

warnings.simplefilter("ignore", category=DeprecationWarning)


class Runner:
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)

    def __init__(self, file, analysis):
        self.config = None
        self.file = file
        logging.basicConfig(format='%(levelname)s: %(message)s')
        self.__load()

        Sources.RUNNER = self
        self.analysis_name = analysis
        self.current_pipeline_name = None
        self.items = {}
        self.dataset = DatasetMaker(self.config['datasets'])
        self.model_execute = ModelExecute(self)

    def __load(self):
        with open(os.path.join(PROJECT, self.file)) as f:
            self.config = self.yaml.load(f)

        # Convert hashes and sources to be strings
        for title, pipeline in self.config['pipelines'].items():
            for i in range(len(pipeline)):
                pipeline[i]['hash'] = str(pipeline[i]['hash'])

                if 'source' in pipeline[i]:
                    if isinstance(pipeline[i]['source'], list):
                        pipeline[i]['source'] = [str(source) for source in pipeline[i]['source']]
                    else:
                        pipeline[i]['source'] = str(pipeline[i]['source'])

                if pipeline[i]['type'] == 'model':
                    for j in range(len(pipeline[i]['runs'])):
                        pipeline[i]['runs'][j]['hash'] = str(pipeline[i]['runs'][j]['hash'])

    def __save(self):
        with open(os.path.join(PROJECT, self.file), 'w') as w:
            self.yaml.dump(self.config, w)

    def clean_pipeline(self, title):
        path = os.path.join(DATA_PROCESSED, self.analysis_name, title)
        if os.path.exists(path):
            shutil.rmtree(path)

        path = os.path.join(RESULTS, self.analysis_name, title)
        if os.path.exists(path):
            shutil.rmtree(path)

    def execute_pipeline(self, title, until=None):
        self.current_pipeline_name = title
        for item in self.config['pipelines'][title]:
            if until is not None and item['hash'] == str(until):
                print('Hit until point: ' + str(until) + '; stopping.')
                break

            self.execute(item)

        print('Completed pipeline ' + title)

    def get_dataset(self, title):
        return self.dataset.get_dataset(title)

    def execute(self, item):
        class_def = ClassDef.get_class(item)
        for run in item['runs']:
            parameters = {**item.get('parameters', {}), **run.get('parameters', {})}
            if 'sources' in run or 'source' in run:
                parameters['sources'] = Sources.get_sources(run, self.items)
            else:
                parameters['sources'] = Sources.get_sources(item, self.items)
            parameters['path'] = [self.analysis_name, self.current_pipeline_name, item['hash'], run['hash']]

            if item['hash'] not in self.items:
                self.items[item['hash']] = {}

            if item['type'] == 'transform':
                item_instance = class_def(**parameters)
                self.items[item['hash']][run['hash']] = item_instance
                Transformer.transform(item_instance)
            elif item['type'] == 'model':
                model = self.model_execute.run_model(item, run, class_def, parameters)
                self.items[item['hash']][run['hash']] = model
            else:
                logging.error('Undefined type "' + item['type'] + '".')
