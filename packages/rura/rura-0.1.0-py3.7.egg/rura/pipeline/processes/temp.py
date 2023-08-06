from rura.pipeline.process import Process


class TempProcess(Process):
    def run(self, model):
        # Get the train and val data
        x_train, y_train, x_val, y_val, x_test, y_test = model.sources[0].get_data(
            ['train_x', 'train_y', 'val_x', 'val_y', 'test_x', 'test_y'], allow_none=True)

        # TODO - Rename to compute_parameters_data
        model.set_parameters_data(x_train, y_train, x_val, y_val, x_test, y_test)

        # Build the model
        model.build()

        # Officially log parameters
        # TODO - Auto log stuff from the init function
        model.log_parameters()

        # Fit the model (send validation as an optional parameter since some models dont use it)
        model.fit(x_train, y_train, x_val=x_val, y_val=y_val)

        model.fit_metrics(x_train, y_train, x_val=x_val, y_val=y_val)

        model.log_model()

        self.extra_metrics(model, x_train, y_train, x_val, y_val, x_test, y_test)

    def extra_metrics(self, model, x_train, y_train, x_val, y_val, x_test, y_test):
        pass
