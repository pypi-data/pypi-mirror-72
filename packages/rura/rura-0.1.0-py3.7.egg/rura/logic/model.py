from rura.pipeline.processes.convert import TrainConvertProcess
from rura.pipeline.processes.suicide import SuicideProcess
from rura.pipeline.processes.temp import TempProcess

from rura.pipeline.processes.vec_nn import VecNNProcess
from rura.tracker import Tracker


class ModelExecute:
    def __init__(self, runner):
        self.runner = runner

    def get_process(self, item):
        process_name = item.get('process', None)
        if process_name == 'TrainConvert':
            return TrainConvertProcess()
        elif process_name == 'VecNN':
            return VecNNProcess()
        elif process_name == 'Suicide':
            return SuicideProcess()

        return TempProcess()

    def run_model(self, item, run, model_class, parameters):
        Tracker.setup()
        exp_name = self.runner.analysis_name + ':' + self.runner.current_pipeline_name + ':'
        exp_name += str(item.get('base', 'None')) + ':' + str(item['func']) + ':' + item['hash']
        Tracker.set_experiment(exp_name)

        print('Running model ' + item['hash'] + '...')
        process = self.get_process(item)

        model = model_class(**parameters)

        if model.is_complete():
            print('Skipping run ' + run['hash'] + '; already exists.')
            model.load_files()
            model.load()
            return model

        # TODO - Save the run_id to the yaml file
        if Tracker.is_logging():
            run_id = Tracker.start_run(run['hash']).info.run_id

        print('Processing run ' + run['hash'] + '...')
        process.run_id = run['hash']
        process.run(model)

        Tracker.end_run()
        return model
