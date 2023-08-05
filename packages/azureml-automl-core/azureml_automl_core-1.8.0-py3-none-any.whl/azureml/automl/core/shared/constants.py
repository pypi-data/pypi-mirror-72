# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Defines automated ML constants used in Azure Machine Learning."""
import sys


class SupportedModels:
    """Defines customer-facing names for algorithms supported by automated ML in Azure Machine Learning."""

    class Classification:
        """Defines classification algorithm names."""

        LogisticRegression = 'LogisticRegression'
        SGDClassifier = 'SGD'
        MultinomialNB = 'MultinomialNaiveBayes'
        BernoulliNB = 'BernoulliNaiveBayes'
        SupportVectorMachine = 'SVM'
        LinearSupportVectorMachine = 'LinearSVM'
        KNearestNeighborsClassifier = 'KNN'
        DecisionTree = 'DecisionTree'
        RandomForest = 'RandomForest'
        ExtraTrees = 'ExtremeRandomTrees'
        LightGBMClassifier = 'LightGBM'
        GradientBoosting = 'GradientBoosting'
        TensorFlowDNNClassifier = 'TensorFlowDNN'
        TensorFlowLinearClassifier = 'TensorFlowLinearClassifier'
        XGBoostClassifier = 'XGBoostClassifier'
        AveragedPerceptronClassifier = 'AveragedPerceptronClassifier'

    class Regression:
        """Defines regression algorithm names."""

        ElasticNet = 'ElasticNet'
        GradientBoostingRegressor = 'GradientBoosting'
        DecisionTreeRegressor = 'DecisionTree'
        KNearestNeighborsRegressor = 'KNN'
        LassoLars = 'LassoLars'
        SGDRegressor = 'SGD'
        RandomForestRegressor = 'RandomForest'
        ExtraTreesRegressor = 'ExtremeRandomTrees'
        LightGBMRegressor = 'LightGBM'
        TensorFlowLinearRegressor = 'TensorFlowLinearRegressor'
        TensorFlowDNNRegressor = 'TensorFlowDNN'
        XGBoostRegressor = 'XGBoostRegressor'
        FastLinearRegressor = 'FastLinearRegressor'
        OnlineGradientDescentRegressor = 'OnlineGradientDescentRegressor'

    class Forecasting(Regression):
        """Defines forecasting algorithm names."""

        AutoArima = 'AutoArima'
        Prophet = 'Prophet'
        TCNForecaster = 'TCNForecaster'


class ModelClassNames:
    """Defines class names for models.

    These are model wrapper class names in the pipeline specs.
    """

    class ClassificationModelClassNames:
        """Defines classification model names."""

        LogisticRegression = 'LogisticRegression'
        SGDClassifier = 'SGDClassifierWrapper'
        MultinomialNB = 'NBWrapper'
        BernoulliNB = 'NBWrapper'  # BernoulliNB use NBWrapper as classname
        SupportVectorMachine = 'SVCWrapper'
        LinearSupportVectorMachine = 'LinearSVMWrapper'
        KNearestNeighborsClassifier = 'KNeighborsClassifier'
        DecisionTree = 'DecisionTreeClassifier'
        RandomForest = 'RandomForestClassifier'
        ExtraTrees = 'ExtraTreesClassifier'
        LightGBMClassifier = 'LightGBMClassifier'
        GradientBoosting = 'GradientBoostingClassifier'
        TensorFlowDNNClassifier = 'TFDNNClassifierWrapper'
        TensorFlowLinearClassifier = 'TFLinearClassifierWrapper'
        XGBoostClassifier = 'XGBoostClassifier'
        NimbusMLAveragedPerceptronClassifier = 'NimbusMlAveragedPerceptronClassifier'
        NimbusMLLinearSVMClassifier = 'NimbusMlLinearSVMClassifier'
        CatBoostClassifier = 'CatBoostClassifier'
        AveragedPerceptronMulticlassClassifier = 'AveragedPerceptronMulticlassClassifier'
        LinearSvmMulticlassClassifier = 'LinearSvmMulticlassClassifier'

    class RegressionModelClassNames:
        """Defines regression model names."""

        ElasticNet = 'ElasticNet'
        GradientBoostingRegressor = 'GradientBoostingRegressor'
        DecisionTreeRegressor = 'DecisionTreeRegressor'
        KNearestNeighborsRegressor = 'KNeighborsRegressor'
        LassoLars = 'LassoLars'
        SGDRegressor = 'SGDRegressor'
        RandomForestRegressor = 'RandomForestRegressor'
        ExtraTreesRegressor = 'ExtraTreesRegressor'
        LightGBMRegressor = 'LightGBMRegressor'
        TensorFlowLinearRegressor = 'TFLinearRegressorWrapper'
        TensorFlowDNNRegressor = 'TFDNNRegressorWrapper'
        XGBoostRegressor = 'XGBoostRegressor'
        NimbusMLFastLinearRegressor = 'NimbusMlFastLinearRegressor'
        NimbusMLOnlineGradientDescentRegressor = 'NimbusMlOnlineGradientDescentRegressor'
        CatBoostRegressor = 'CatBoostRegressor'

    class ForecastingModelClassNames(RegressionModelClassNames):
        """Defines forecasting model names."""

        AutoArima = 'AutoArima'
        Prophet = 'Prophet'
        TCNForecaster = 'TCNForecaster'


class LegacyModelNames:
    """
    Defines names for all models supported by the Miro recommender in Automated ML.

    These names are still used to refer to objects in the Miro database, but are not
    used by any Automated ML clients.
    """

    class ClassificationLegacyModelNames:
        """Defines names for all Miro classification models."""

        LogisticRegression = 'logistic regression'
        SGDClassifier = 'SGD classifier'
        MultinomialNB = 'MultinomialNB'
        BernoulliNB = 'BernoulliNB'
        SupportVectorMachine = 'SVM'
        LinearSupportVectorMachine = 'LinearSVM'
        KNearestNeighborsClassifier = 'kNN'
        DecisionTree = 'DT'
        RandomForest = 'RF'
        ExtraTrees = 'extra trees'
        LightGBMClassifier = 'lgbm_classifier'
        GradientBoosting = 'gradient boosting'
        TensorFlowDNNClassifier = 'TF DNNClassifier'
        TensorFlowLinearClassifier = 'TF LinearClassifier'
        XGBoostClassifier = 'xgboost classifier'
        NimbusMLAveragedPerceptronClassifier = 'averaged perceptron classifier'
        NimbusMLLinearSVMClassifier = 'nimbusml linear svm classifier'
        CatBoostClassifier = 'catboost_classifier'

    class RegressionLegacyModelNames:
        """Defines names for all Miro regression models."""

        ElasticNet = 'Elastic net'
        GradientBoostingRegressor = 'Gradient boosting regressor'
        DecisionTreeRegressor = 'DT regressor'
        KNearestNeighborsRegressor = 'kNN regressor'
        LassoLars = 'Lasso lars'
        SGDRegressor = 'SGD regressor'
        RandomForestRegressor = 'RF regressor'
        ExtraTreesRegressor = 'extra trees regressor'
        LightGBMRegressor = 'lightGBM regressor'
        TensorFlowLinearRegressor = 'TF LinearRegressor'
        TensorFlowDNNRegressor = 'TF DNNRegressor'
        XGBoostRegressor = 'xgboost regressor'
        NimbusMLFastLinearRegressor = 'nimbusml fast linear regressor'
        NimbusMLOnlineGradientDescentRegressor = 'nimbusml online gradient descent regressor'
        CatBoostRegressor = 'catboost_regressor'

    class ForecastingLegacyModelNames(RegressionLegacyModelNames):
        """Defines names for all forecasting legacy models."""

        pass


ARTIFACT_TAG = "artifact"
MODEL_EXPLANATION_TAG = "model_explanation"
CHILD_RUNS_SUMMARY_PATH = "outputs/child_runs_summary.json"
MODEL_PATH = "outputs/model.pkl"
MODEL_PATH_TRAIN = "outputs/internal_cross_validated_models.pkl"
MODEL_PATH_ONNX = "outputs/model.onnx"
MODEL_RESOURCE_PATH_ONNX = "outputs/model_onnx.json"
DEPENDENCIES_PATH = "outputs/env_dependencies.json"
CONDA_ENV_FILE_PATH = "outputs/conda_env_v_1_0_0.yml"
SCORING_FILE_PATH = "outputs/scoring_file_v_1_0_0.py"
PIPELINE_GRAPH_PATH = "outputs/pipeline_graph.json"
PIPELINE_GRAPH_VERSION = '1.0.0'
MAX_ITERATIONS = 1000
MAX_SAMPLES_BLACKLIST = 5000
MAX_SAMPLES_BLACKLIST_ALGOS = [SupportedModels.Classification.KNearestNeighborsClassifier,
                               SupportedModels.Regression.KNearestNeighborsRegressor,
                               SupportedModels.Classification.SupportVectorMachine]
EARLY_STOPPING_NUM_LANDMARKS = 20
MULTINOMIAL_ALGO_TAG = 'Multinomial'

"""Names of algorithms that do not support sample weights."""
Sample_Weights_Unsupported = {
    ModelClassNames.RegressionModelClassNames.ElasticNet,
    ModelClassNames.ClassificationModelClassNames.KNearestNeighborsClassifier,
    ModelClassNames.RegressionModelClassNames.KNearestNeighborsRegressor,
    ModelClassNames.RegressionModelClassNames.LassoLars,
}
"""Algorithm names that we must force to run in single threaded mode."""
SINGLE_THREADED_ALGORITHMS = [
    ModelClassNames.ClassificationModelClassNames.KNearestNeighborsClassifier,
    ModelClassNames.RegressionModelClassNames.KNearestNeighborsRegressor
]


class EnsembleConstants(object):
    """Defines constants used for Ensemble iterations."""

    VOTING_ENSEMBLE_PIPELINE_ID = "__AutoML_Ensemble__"
    STACK_ENSEMBLE_PIPELINE_ID = "__AutoML_Stack_Ensemble__"
    ENSEMBLE_PIPELINE_IDS = [VOTING_ENSEMBLE_PIPELINE_ID, STACK_ENSEMBLE_PIPELINE_ID]
    # by default, we'll use 20% of the training data (when doing TrainValidation split) for training the meta learner
    DEFAULT_TRAIN_PERCENTAGE_FOR_STACK_META_LEARNER = 0.2

    class StackMetaLearnerAlgorithmNames(object):
        """Defines algorithms supported for training the Stack Ensemble meta learner."""

        LogisticRegression = SupportedModels.Classification.LogisticRegression
        LogisticRegressionCV = "LogisticRegressionCV"
        LightGBMClassifier = SupportedModels.Classification.LightGBMClassifier
        ElasticNet = SupportedModels.Regression.ElasticNet
        ElasticNetCV = "ElasticNetCV"
        LightGBMRegressor = SupportedModels.Regression.LightGBMRegressor
        LinearRegression = "LinearRegression"
        ALL = [
            LogisticRegression,
            LogisticRegressionCV,
            LightGBMClassifier,
            ElasticNet,
            ElasticNetCV,
            LightGBMRegressor,
            LinearRegression]


class ModelName:
    """Defines a model name that includes customer, legacy, and class names."""

    def __init__(self, customer_model_name, legacy_model_name, model_class_name, is_deprecated=False):
        """Init ModelName."""
        self.customer_model_name = customer_model_name
        self.legacy_model_name = legacy_model_name
        self.model_class_name = model_class_name
        self.is_deprecated = is_deprecated

    def __repr__(self):
        return self.customer_model_name


class SupportedModelNames:
    """Defines supported models where each model has a customer name, legacy model name, and model class name."""

    SupportedClassificationModelList = [
        ModelName(
            SupportedModels.Classification.
            LogisticRegression,
            LegacyModelNames.ClassificationLegacyModelNames.LogisticRegression,
            ModelClassNames.ClassificationModelClassNames.LogisticRegression),
        ModelName(
            SupportedModels.Classification.
            SGDClassifier,
            LegacyModelNames.ClassificationLegacyModelNames.SGDClassifier,
            ModelClassNames.ClassificationModelClassNames.SGDClassifier),
        ModelName(
            SupportedModels.Classification.
            MultinomialNB,
            LegacyModelNames.ClassificationLegacyModelNames.MultinomialNB,
            ModelClassNames.ClassificationModelClassNames.MultinomialNB),
        ModelName(
            SupportedModels.Classification.
            BernoulliNB,
            LegacyModelNames.ClassificationLegacyModelNames.BernoulliNB,
            ModelClassNames.ClassificationModelClassNames.BernoulliNB),
        ModelName(
            SupportedModels.Classification.
            SupportVectorMachine,
            LegacyModelNames.ClassificationLegacyModelNames.
            SupportVectorMachine,
            ModelClassNames.ClassificationModelClassNames.SupportVectorMachine),
        ModelName(
            SupportedModels.Classification.
            LinearSupportVectorMachine,
            LegacyModelNames.ClassificationLegacyModelNames.
            LinearSupportVectorMachine,
            ModelClassNames.ClassificationModelClassNames.
            LinearSupportVectorMachine),
        ModelName(
            SupportedModels.Classification.
            KNearestNeighborsClassifier,
            LegacyModelNames.ClassificationLegacyModelNames.
            KNearestNeighborsClassifier,
            ModelClassNames.ClassificationModelClassNames.
            KNearestNeighborsClassifier),
        ModelName(
            SupportedModels.Classification.
            DecisionTree,
            LegacyModelNames.ClassificationLegacyModelNames.DecisionTree,
            ModelClassNames.ClassificationModelClassNames.DecisionTree),
        ModelName(
            SupportedModels.Classification.
            RandomForest,
            LegacyModelNames.ClassificationLegacyModelNames.RandomForest,
            ModelClassNames.ClassificationModelClassNames.RandomForest),
        ModelName(
            SupportedModels.Classification.
            ExtraTrees,
            LegacyModelNames.ClassificationLegacyModelNames.ExtraTrees,
            ModelClassNames.ClassificationModelClassNames.ExtraTrees),
        ModelName(
            SupportedModels.Classification.
            LightGBMClassifier,
            LegacyModelNames.ClassificationLegacyModelNames.LightGBMClassifier,
            ModelClassNames.ClassificationModelClassNames.LightGBMClassifier),
        ModelName(
            SupportedModels.Classification.
            XGBoostClassifier,
            LegacyModelNames.ClassificationLegacyModelNames.XGBoostClassifier,
            ModelClassNames.ClassificationModelClassNames.XGBoostClassifier),
        ModelName(
            SupportedModels.Classification.AveragedPerceptronClassifier,
            LegacyModelNames.ClassificationLegacyModelNames.NimbusMLAveragedPerceptronClassifier,
            ModelClassNames.ClassificationModelClassNames.NimbusMLAveragedPerceptronClassifier),
        ModelName(
            SupportedModels.Classification.AveragedPerceptronClassifier,
            LegacyModelNames.ClassificationLegacyModelNames.NimbusMLAveragedPerceptronClassifier,
            ModelClassNames.ClassificationModelClassNames.AveragedPerceptronMulticlassClassifier),
        ModelName(
            SupportedModels.Classification.
            GradientBoosting,
            LegacyModelNames.ClassificationLegacyModelNames.GradientBoosting,
            ModelClassNames.ClassificationModelClassNames.GradientBoosting),
        ModelName(
            SupportedModels.Classification.
            TensorFlowDNNClassifier,
            LegacyModelNames.ClassificationLegacyModelNames.
            TensorFlowDNNClassifier,
            ModelClassNames.ClassificationModelClassNames.
            TensorFlowDNNClassifier,
            is_deprecated=True),
        ModelName(
            SupportedModels.Classification.
            TensorFlowLinearClassifier,
            LegacyModelNames.ClassificationLegacyModelNames.
            TensorFlowLinearClassifier,
            ModelClassNames.ClassificationModelClassNames.
            TensorFlowLinearClassifier,
            is_deprecated=True)]

    SupportedRegressionModelList = [
        ModelName(
            SupportedModels.Regression.ElasticNet,
            LegacyModelNames.RegressionLegacyModelNames.ElasticNet,
            ModelClassNames.RegressionModelClassNames.ElasticNet),
        ModelName(
            SupportedModels.Regression.
            GradientBoostingRegressor,
            LegacyModelNames.RegressionLegacyModelNames.
            GradientBoostingRegressor,
            ModelClassNames.RegressionModelClassNames.
            GradientBoostingRegressor),
        ModelName(
            SupportedModels.Regression.
            DecisionTreeRegressor,
            LegacyModelNames.RegressionLegacyModelNames.DecisionTreeRegressor,
            ModelClassNames.RegressionModelClassNames.DecisionTreeRegressor),
        ModelName(
            SupportedModels.Regression.
            KNearestNeighborsRegressor,
            LegacyModelNames.RegressionLegacyModelNames.
            KNearestNeighborsRegressor,
            ModelClassNames.RegressionModelClassNames.
            KNearestNeighborsRegressor),
        ModelName(
            SupportedModels.Regression.LassoLars,
            LegacyModelNames.RegressionLegacyModelNames.LassoLars,
            ModelClassNames.RegressionModelClassNames.LassoLars),
        ModelName(
            SupportedModels.Regression.
            SGDRegressor,
            LegacyModelNames.RegressionLegacyModelNames.SGDRegressor,
            ModelClassNames.RegressionModelClassNames.SGDRegressor),
        ModelName(
            SupportedModels.Regression.
            RandomForestRegressor,
            LegacyModelNames.RegressionLegacyModelNames.RandomForestRegressor,
            ModelClassNames.RegressionModelClassNames.RandomForestRegressor),
        ModelName(
            SupportedModels.Regression.
            ExtraTreesRegressor,
            LegacyModelNames.RegressionLegacyModelNames.ExtraTreesRegressor,
            ModelClassNames.RegressionModelClassNames.ExtraTreesRegressor),
        ModelName(
            SupportedModels.Regression.
            LightGBMRegressor,
            LegacyModelNames.RegressionLegacyModelNames.LightGBMRegressor,
            ModelClassNames.RegressionModelClassNames.LightGBMRegressor),
        ModelName(
            SupportedModels.Regression.
            XGBoostRegressor,
            LegacyModelNames.RegressionLegacyModelNames.XGBoostRegressor,
            ModelClassNames.RegressionModelClassNames.XGBoostRegressor),
        ModelName(
            SupportedModels.Regression.FastLinearRegressor,
            LegacyModelNames.RegressionLegacyModelNames.NimbusMLFastLinearRegressor,
            ModelClassNames.RegressionModelClassNames.NimbusMLFastLinearRegressor),
        ModelName(
            SupportedModels.Regression.OnlineGradientDescentRegressor,
            LegacyModelNames.RegressionLegacyModelNames.NimbusMLOnlineGradientDescentRegressor,
            ModelClassNames.RegressionModelClassNames.NimbusMLOnlineGradientDescentRegressor),
        ModelName(
            SupportedModels.Regression.
            TensorFlowLinearRegressor,
            LegacyModelNames.RegressionLegacyModelNames.
            TensorFlowLinearRegressor,
            ModelClassNames.RegressionModelClassNames.
            TensorFlowLinearRegressor,
            is_deprecated=True),
        ModelName(
            SupportedModels.Regression.
            TensorFlowDNNRegressor,
            LegacyModelNames.RegressionLegacyModelNames.TensorFlowDNNRegressor,
            ModelClassNames.RegressionModelClassNames.TensorFlowDNNRegressor,
            is_deprecated=True)]

    SupportedForecastingModelList = SupportedRegressionModelList + [
        ModelName(
            SupportedModels.Forecasting.AutoArima,
            None,
            ModelClassNames.ForecastingModelClassNames.AutoArima),
        ModelName(
            SupportedModels.Forecasting.Prophet,
            None,
            ModelClassNames.ForecastingModelClassNames.Prophet),
        ModelName(
            SupportedModels.Forecasting.TCNForecaster,
            None,
            ModelClassNames.ForecastingModelClassNames.TCNForecaster)]

    SupportedStreamingModelList = [
        ModelName(
            SupportedModels.Classification.AveragedPerceptronClassifier,
            LegacyModelNames.ClassificationLegacyModelNames.NimbusMLAveragedPerceptronClassifier,
            ModelClassNames.ClassificationModelClassNames.AveragedPerceptronMulticlassClassifier),
        ModelName(
            SupportedModels.Classification.LinearSupportVectorMachine,
            LegacyModelNames.ClassificationLegacyModelNames.NimbusMLLinearSVMClassifier,
            ModelClassNames.ClassificationModelClassNames.LinearSupportVectorMachine),
        ModelName(
            SupportedModels.Regression.FastLinearRegressor,
            LegacyModelNames.RegressionLegacyModelNames.NimbusMLFastLinearRegressor,
            ModelClassNames.RegressionModelClassNames.NimbusMLFastLinearRegressor),
        ModelName(
            SupportedModels.Regression.OnlineGradientDescentRegressor,
            LegacyModelNames.RegressionLegacyModelNames.NimbusMLOnlineGradientDescentRegressor,
            ModelClassNames.RegressionModelClassNames.NimbusMLOnlineGradientDescentRegressor),
    ]


class ModelNameMappings:
    """Defines model name mappings."""

    CustomerFacingModelToLegacyModelMapClassification = dict(zip(
        [model.customer_model_name for model in SupportedModelNames.
            SupportedClassificationModelList],
        [model.legacy_model_name for model in SupportedModelNames.
            SupportedClassificationModelList]))

    CustomerFacingModelToLegacyModelMapRegression = dict(zip(
        [model.customer_model_name for model in SupportedModelNames.
            SupportedRegressionModelList],
        [model.legacy_model_name for model in SupportedModelNames.
            SupportedRegressionModelList]))

    CustomerFacingModelToLegacyModelMapForecasting = dict(zip(
        [model.customer_model_name for model in SupportedModelNames.
            SupportedForecastingModelList],
        [model.legacy_model_name for model in SupportedModelNames.
            SupportedForecastingModelList]))

    CustomerFacingModelToClassNameModelMapClassification = dict(zip(
        [model.customer_model_name for model in SupportedModelNames.
            SupportedClassificationModelList],
        [model.model_class_name for model in SupportedModelNames.
            SupportedClassificationModelList]))

    CustomerFacingModelToClassNameModelMapRegression = dict(zip(
        [model.customer_model_name for model in SupportedModelNames.
            SupportedRegressionModelList],
        [model.model_class_name for model in SupportedModelNames.
            SupportedRegressionModelList]))

    CustomerFacingModelToClassNameModelMapForecasting = dict(zip(
        [model.customer_model_name for model in SupportedModelNames.
            SupportedForecastingModelList],
        [model.model_class_name for model in SupportedModelNames.
            SupportedForecastingModelList]))

    ClassNameToCustomerFacingModelMapClassification = dict(zip(
        [model.model_class_name for model in SupportedModelNames.
            SupportedClassificationModelList],
        [model.customer_model_name for model in SupportedModelNames.
            SupportedClassificationModelList]))

    ClassNameToCustomerFacingModelMapRegression = dict(zip(
        [model.model_class_name for model in SupportedModelNames.
            SupportedRegressionModelList],
        [model.customer_model_name for model in SupportedModelNames.
            SupportedRegressionModelList]))

    ClassNameToCustomerFacingModelMapForecasting = dict(zip(
        [model.model_class_name for model in SupportedModelNames.
            SupportedForecastingModelList],
        [model.customer_model_name for model in SupportedModelNames.
            SupportedForecastingModelList]))


class ModelCategories:
    """Defines categories for models."""

    PARTIAL_FIT = {
        ModelClassNames.ClassificationModelClassNames.MultinomialNB,
        ModelClassNames.ClassificationModelClassNames.BernoulliNB,
        ModelClassNames.ClassificationModelClassNames.SGDClassifier,
        ModelClassNames.ClassificationModelClassNames.TensorFlowLinearClassifier,
        ModelClassNames.ClassificationModelClassNames.TensorFlowDNNClassifier,
        ModelClassNames.ClassificationModelClassNames.NimbusMLAveragedPerceptronClassifier,
        ModelClassNames.ClassificationModelClassNames.NimbusMLLinearSVMClassifier,
        ModelClassNames.ClassificationModelClassNames.AveragedPerceptronMulticlassClassifier,
        ModelClassNames.ClassificationModelClassNames.LinearSvmMulticlassClassifier,
        ModelClassNames.RegressionModelClassNames.NimbusMLFastLinearRegressor,
        ModelClassNames.RegressionModelClassNames.NimbusMLOnlineGradientDescentRegressor,
        ModelClassNames.RegressionModelClassNames.SGDRegressor,
        ModelClassNames.RegressionModelClassNames.TensorFlowLinearRegressor,
        ModelClassNames.RegressionModelClassNames.TensorFlowDNNRegressor
    }


class PreprocessorCategories:
    """Defines categories for preprocessors."""

    PARTIAL_FIT = {'StandardScaler', 'MinMaxScaler', 'MaxAbsScaler'}


class Defaults:
    """Defines default values for pipelines."""

    DEFAULT_PIPELINE_SCORE = float('NaN')  # Jasmine and 016N
    INVALID_PIPELINE_VALIDATION_SCORES = {}
    INVALID_PIPELINE_FITTED = ''
    INVALID_PIPELINE_OBJECT = None


class RunState:
    """Defines states a run can be in."""

    START_RUN = 'running'
    FAIL_RUN = 'failed'
    CANCEL_RUN = 'canceled'
    COMPLETE_RUN = 'completed'
    PREPARE_RUN = 'preparing'


class API:
    """Defines names for the Azure Machine Learning API operations that can be performed."""

    CreateExperiment = 'Create Experiment'
    CreateParentRun = 'Create Parent Run'
    GetNextPipeline = 'Get Pipeline'
    SetParentRunStatus = 'Set Parent Run Status'
    StartRemoteRun = 'Start Remote Run'
    StartRemoteSnapshotRun = 'Start Remote Snapshot Run'
    CancelChildRun = 'Cancel Child Run'
    StartChildRun = 'Start Child Run'
    SetRunProperties = 'Set Run Properties'
    LogMetrics = 'Log Metrics'
    InstantiateRun = 'Get Run'
    GetChildren = 'Get Children'


class AcquisitionFunction:
    """Defines names for all acquisition functions used to select the next pipeline.

    The default is EI (expected improvement).
    """

    EI = "EI"
    PI = "PI"
    UCB = "UCB"
    THOMPSON = "thompson"
    EXPECTED = "expected"

    FULL_SET = {EI, PI, UCB, THOMPSON, EXPECTED}


class Status:
    """Defines possible child run states."""

    NotStarted = 'Not Started'
    Started = 'Started'
    InProgress = 'In Progress'
    Completed = 'Completed'
    Terminated = 'Terminated'

    FULL_SET = {NotStarted, Started, InProgress, Completed, Terminated}

    @classmethod
    def pretty(cls, metric):
        """
        Verbose printing of AutoMLRun statuses.

        :param metric: The metric to print.
        :type metric: azureml.train.automl.constants.Status
        :return: Pretty print of the metric.
        :rtype: str
        """
        return {
            cls.Started: "Started",
            cls.InProgress: "In Progress running one of the child iterations.",
            cls.Completed: "Completed",
            cls.Terminated: "Terminated before finishing execution",
        }[metric]


class FitPipelineComponentName:
    """Constants for the FitPipeline Component names."""

    PREPRARE_DATA = "PrepareData"
    COMPLETE_RUN = "CompleteRun"


class PipelineParameterConstraintCheckStatus:
    """Defines values indicating whether pipeline is valid."""

    VALID = 0
    REMOVE = 1
    REJECTPIPELINE = 2


class OptimizerObjectives:
    """Defines nthe objectives an algorithm can have relative to a metric.

    Some metrics should be maximized and some should be minimized.
    """

    MAXIMIZE = "maximize"
    MINIMIZE = "minimize"
    NA = 'NA'

    FULL_SET = {MAXIMIZE, MINIMIZE, NA}


class Optimizer:
    """Defines the categories of pipeline prediction algorithms used.

    - "random" provides a baseline by selecting a pipeline randomly
    - "lvm" uses latent variable models to predict probable next pipelines
      given performance on previous pipelines.
    """

    Random = "random"
    LVM = "lvm"

    FULL_SET = {Random, LVM}


class Tasks:
    """Defines types of machine learning tasks supported by automated ML."""

    CLASSIFICATION = 'classification'
    REGRESSION = 'regression'
    IMAGE_CLASSIFICATION = 'image-classification'
    IMAGE_MULTI_LABEL_CLASSIFICATION = 'image-multi-labeling'
    IMAGE_OBJECT_DETECTION = 'image-object-detection'
    ALL_IMAGE = [IMAGE_CLASSIFICATION, IMAGE_MULTI_LABEL_CLASSIFICATION, IMAGE_OBJECT_DETECTION]

    ALL_MIRO = [CLASSIFICATION, REGRESSION]
    ALL = ALL_MIRO + ALL_IMAGE


class ClientErrors:
    """Defines client errors that can occur when violating user-specified cost constraints."""

    EXCEEDED_TIME_CPU = "CPU time exceeded the specified limit. Please consider increasing the CPU time limit."
    EXCEEDED_TIME = "Wall clock time exceeded the specified limit. Please consider increasing the time limit."
    EXCEEDED_ITERATION_TIMEOUT_MINUTES = "Iteration timeout reached, skipping the iteration. " \
                                         "Please consider increasing iteration_timeout_minutes."
    EXCEEDED_EXPERIMENT_TIMEOUT_MINUTES = "Experiment timeout reached, skipping the iteration. " \
                                          "Please consider increasing experiment_timeout_minutes."
    EXCEEDED_MEMORY = "Memory usage exceeded the specified limit or was killed by the OS due to low memory " \
                      "conditions. Please consider increasing available memory."
    SUBPROCESS_ERROR = "The subprocess was killed due to an error."
    GENERIC_ERROR = "An unknown error occurred."

    ALL_ERRORS = {
        EXCEEDED_TIME_CPU, EXCEEDED_TIME, EXCEEDED_ITERATION_TIMEOUT_MINUTES, EXCEEDED_EXPERIMENT_TIMEOUT_MINUTES,
        EXCEEDED_MEMORY, SUBPROCESS_ERROR, GENERIC_ERROR
    }
    TIME_ERRORS = {
        EXCEEDED_TIME_CPU, EXCEEDED_TIME, EXCEEDED_ITERATION_TIMEOUT_MINUTES, EXCEEDED_EXPERIMENT_TIMEOUT_MINUTES
    }


class ServerStatus:
    """Defines server status values."""

    OK = 'ok'
    INCREASE_TIME_THRESHOLD = 'threshold'


class TimeConstraintEnforcement:
    """Enumeration of time contraint enforcement modes."""

    TIME_CONSTRAINT_NONE = 0
    TIME_CONSTRAINT_PER_ITERATION = 1
    TIME_CONSTRAINT_TOTAL = 2
    TIME_CONSTRAINT_TOTAL_AND_ITERATION = 3


class PipelineCost:
    """Defines cost model modes.

    - COST_NONE returns all predicted pipelines
    - COST_FILTER returns only pipelines that were predicted by cost models
      to meet the user-specified cost conditions
    - COST_SCALE divides the acquisition function score by the predicted time
    """

    COST_NONE = 0
    COST_FILTER = 1
    COST_SCALE_ACQUISITION = 2  # no filtering, so not great
    COST_SCALE_AND_FILTER = 3  # a little too greedy
    COST_SCALE_THEN_FILTER = 4  # annealing accomplishes the same thing more smoothly
    COST_ALTERNATE = 5  # switch between annealing and filtering, useful for debugging
    COST_SCALE_AND_FILTER_ANNEAL = 6  # scale acq_fn score by time but reduce impact of time
    # as the run is closer to completion because otherwise we also pick fast models
    COST_PROBABILITY = 7  # use a probability to filter out models
    COST_PROBABILITY_SAMPLE = 8  # sample models with probability
    # equal to the chance the model runs without timing out
    COST_MODEL_ALL_ANNEALING = {COST_SCALE_AND_FILTER_ANNEAL,
                                COST_PROBABILITY,
                                COST_PROBABILITY_SAMPLE}
    COST_MODEL_ALL_SCALE = COST_MODEL_ALL_ANNEALING | {COST_SCALE_ACQUISITION,
                                                       COST_SCALE_AND_FILTER,
                                                       COST_SCALE_THEN_FILTER,
                                                       COST_ALTERNATE}
    # TODO: Add a mode that looks at setting timeout to a percentile of the good models
    # because we dont want to restrict to only fast models if we need the expensive models
    # Used to restrict the number of piplines we predict cost for if we want to save time
    # currently set to the same values as the pruned index so no optimization is made
    MAX_COST_PREDICTS = 20000


class IterationTimeout:
    """Defines ways of changing the per_iteration_timeout."""

    TIMEOUT_NONE = 0
    TIMEOUT_SUGGEST_TIMEOUT = 1  # suggest timeout based on problem_info
    TIMEOUT_BEST_TIME = 2  # increase the timeout based on a factor of the best model seen so far
    TIMEOUT_DOUBLING = 3  # start with a low timeout and double it as time goes on
    TIMEOUT_PERCENTILE = 4  # set time to percentile of all models
    TIMEOUT_BEST_TIME_SUGGEST = 5  # TIMEOUT_BEST_TIME + TIMEOUT_SUGGEST_TIMEOUT
    TIMEOUT_DOUBLING_SUGGEST = 6  # TIMEOUT_DOUBLING + TIMEOUT_SUGGEST_TIMEOUT
    TIMEOUT_PERCENTILE_SUGGEST = 7  # TIMEOUT_DOUBLING + TIMEOUT_SUGGEST_TIMEOUT
    TIMEOUT_ALL_SUGGEST = {TIMEOUT_SUGGEST_TIMEOUT, TIMEOUT_BEST_TIME_SUGGEST,
                           TIMEOUT_DOUBLING_SUGGEST, TIMEOUT_PERCENTILE_SUGGEST}


class PipelineMaskProfiles:
    """Defines mask profiles for pipelines."""

    MASK_NONE = 'none'
    MASK_PARTIAL_FIT = 'partial_fit'
    MASK_LGBM_ONLY = 'lgbm'
    MASK_MANY_FEATURES = 'many_features'
    MASK_SPARSE = 'sparse'
    MASK_PRUNE = 'prune'
    MASK_TIME_PRUNE = 'time_prune'
    MASK_RANGE = 'range_mask'
    MASK_INDEX = 'pruned_index_name'

    ALL_MASKS = [
        MASK_NONE,
        MASK_PARTIAL_FIT, MASK_MANY_FEATURES,
        MASK_SPARSE,
        MASK_RANGE]


class SubsamplingTreatment:
    """Defines subsampling treatment in GP."""

    LOG = 'log'
    LINEAR = 'linear'


class SubsamplingSchedule:
    """Defines subsampling strategies."""

    HYPERBAND = 'hyperband'
    HYPERBAND_CLIP = 'hyperband_clip'
    FULL_PCT = 100.0


class EnsembleMethod:
    """Defines ensemble methods."""

    ENSEMBLE_AVERAGE = 'average'
    ENSEMBLE_STACK = 'stack_lr'
    # take the best model from each class, This is what H20 does
    ENSEMBLE_BEST_MODEL = 'best_model'
    # stack, but with a lgbm not a logistic regression
    ENSEMBLE_STACK_LGBM = 'stack_lgbm'
    # take the best model from each cluster of the model's latent space
    ENSEMBLE_LATENT_SPACE = 'latent_space'
    # take the best model from each of the datasets classes
    ENSEMBLE_BEST_CLASS = 'best_class'


class TrainingResultsType:
    """Defines potential results from runners class."""

    # Metrics
    TRAIN_METRICS = 'train'
    VALIDATION_METRICS = 'validation'
    TEST_METRICS = 'test'
    TRAIN_FROM_FULL_METRICS = 'train from full'
    TEST_FROM_FULL_METRICS = 'test from full'
    CV_METRICS = 'CV'
    CV_MEAN_METRICS = 'CV mean'

    # Other useful things
    TRAIN_TIME = 'train time'
    FIT_TIME = 'fit_time'
    PREDICT_TIME = 'predict_time'
    BLOB_TIME = 'blob_time'
    ALL_TIME = {TRAIN_TIME, FIT_TIME, PREDICT_TIME}
    TRAIN_PERCENT = 'train_percent'
    MODELS = 'models'

    # Status:
    TRAIN_VALIDATE_STATUS = 'train validate status'
    TRAIN_FULL_STATUS = 'train full status'
    CV_STATUS = 'CV status'


class Metric:
    """Defines all metrics supported by classification and regression."""

    # Classification
    AUCMacro = 'AUC_macro'
    AUCMicro = 'AUC_micro'
    AUCWeighted = 'AUC_weighted'
    Accuracy = 'accuracy'
    WeightedAccuracy = 'weighted_accuracy'
    BalancedAccuracy = 'balanced_accuracy'
    NormMacroRecall = 'norm_macro_recall'
    LogLoss = 'log_loss'
    F1Micro = 'f1_score_micro'
    F1Macro = 'f1_score_macro'
    F1Weighted = 'f1_score_weighted'
    PrecisionMicro = 'precision_score_micro'
    PrecisionMacro = 'precision_score_macro'
    PrecisionWeighted = 'precision_score_weighted'
    RecallMicro = 'recall_score_micro'
    RecallMacro = 'recall_score_macro'
    RecallWeighted = 'recall_score_weighted'
    AvgPrecisionMicro = 'average_precision_score_micro'
    AvgPrecisionMacro = 'average_precision_score_macro'
    AvgPrecisionWeighted = 'average_precision_score_weighted'
    AccuracyTable = 'accuracy_table'
    ConfusionMatrix = 'confusion_matrix'
    MatthewsCorrelation = 'matthews_correlation'

    # Regression
    ExplainedVariance = 'explained_variance'
    R2Score = 'r2_score'
    Spearman = 'spearman_correlation'
    MAPE = 'mean_absolute_percentage_error'
    SMAPE = 'symmetric_mean_absolute_percentage_error'
    MeanAbsError = 'mean_absolute_error'
    MedianAbsError = 'median_absolute_error'
    RMSE = 'root_mean_squared_error'
    RMSLE = 'root_mean_squared_log_error'
    NormMeanAbsError = 'normalized_mean_absolute_error'
    NormMedianAbsError = 'normalized_median_absolute_error'
    NormRMSE = 'normalized_root_mean_squared_error'
    NormRMSLE = 'normalized_root_mean_squared_log_error'
    Residuals = 'residuals'
    PredictedTrue = 'predicted_true'

    # Forecast
    ForecastMAPE = 'forecast_mean_absolute_percentage_error'
    ForecastSMAPE = 'forecast_symmetric_mean_absolute_percentage_error'
    ForecastResiduals = 'forecast_residuals'

    # Image Object Detection
    MeanAveragePrecision = 'mean_average_precision'

    SCALAR_CLASSIFICATION_SET = {
        AUCMacro, AUCMicro, AUCWeighted, Accuracy,
        WeightedAccuracy, NormMacroRecall, BalancedAccuracy,
        LogLoss, F1Micro, F1Macro, F1Weighted, PrecisionMicro,
        PrecisionMacro, PrecisionWeighted, RecallMicro, RecallMacro,
        RecallWeighted, AvgPrecisionMicro, AvgPrecisionMacro,
        AvgPrecisionWeighted, MatthewsCorrelation
    }

    NONSCALAR_CLASSIFICATION_SET = {
        AccuracyTable, ConfusionMatrix
    }

    CLASSIFICATION_SET = (SCALAR_CLASSIFICATION_SET |
                          NONSCALAR_CLASSIFICATION_SET)

    SCALAR_REGRESSION_SET = {
        ExplainedVariance, R2Score, Spearman, MAPE, MeanAbsError,
        MedianAbsError, RMSE, RMSLE, NormMeanAbsError,
        NormMedianAbsError, NormRMSE, NormRMSLE
    }

    NONSCALAR_REGRESSION_SET = {
        Residuals, PredictedTrue
    }

    REGRESSION_SET = (SCALAR_REGRESSION_SET |
                      NONSCALAR_REGRESSION_SET)

    NONSCALAR_FORECAST_SET = {
        ForecastMAPE, ForecastResiduals
    }

    FORECAST_SET = (NONSCALAR_FORECAST_SET)

    CLASSIFICATION_PRIMARY_SET = {
        Accuracy, AUCWeighted, NormMacroRecall, AvgPrecisionWeighted,
        PrecisionWeighted
    }

    CLASSIFICATION_BALANCED_SET = {
        # this is for metrics where we would recommend using class_weights
        BalancedAccuracy, AUCMacro, NormMacroRecall, AvgPrecisionMacro,
        PrecisionMacro, F1Macro, RecallMacro
    }

    REGRESSION_PRIMARY_SET = {
        Spearman, NormRMSE, R2Score, NormMeanAbsError
    }

    IMAGE_CLASSIFICATION_PRIMARY_SET = {
        Accuracy
    }

    IMAGE_MULTI_LABEL_CLASSIFICATION_PRIMARY_SET = {
        Accuracy
    }

    IMAGE_OBJECT_DETECTION_PRIMARY_SET = {
        MeanAveragePrecision,
    }

    IMAGE_OBJECT_DETECTION_SET = {
        MeanAveragePrecision,
    }

    SAMPLE_WEIGHTS_UNSUPPORTED_SET = {
        WeightedAccuracy, Spearman, MedianAbsError, NormMedianAbsError
    }

    FULL_SET = CLASSIFICATION_SET | REGRESSION_SET | FORECAST_SET | IMAGE_OBJECT_DETECTION_SET
    NONSCALAR_FULL_SET = (NONSCALAR_CLASSIFICATION_SET |
                          NONSCALAR_REGRESSION_SET |
                          NONSCALAR_FORECAST_SET)
    SCALAR_FULL_SET = (SCALAR_CLASSIFICATION_SET |
                       SCALAR_REGRESSION_SET)
    SCALAR_FULL_SET_TIME = (SCALAR_FULL_SET | TrainingResultsType.ALL_TIME)

    # TODO: These types will be removed when the artifact-backed
    # metrics are defined with protobuf
    # Do not use these constants except in artifact-backed metrics
    SCHEMA_TYPE_ACCURACY_TABLE = 'accuracy_table'
    SCHEMA_TYPE_CONFUSION_MATRIX = 'confusion_matrix'
    SCHEMA_TYPE_RESIDUALS = 'residuals'
    SCHEMA_TYPE_PREDICTIONS = 'predictions'
    SCHEMA_TYPE_MAPE = 'mape_table'
    SCHEMA_TYPE_SMAPE = 'smape_table'

    @classmethod
    def pretty(cls, metric):
        """Verbose names for metrics."""
        return {
            cls.AUCMacro: "Macro Area Under The Curve",
            cls.AUCMicro: "Micro Area Under The Curve",
            cls.AUCWeighted: "Weighted Area Under The Curve",
            cls.Accuracy: "Accuracy",
            cls.WeightedAccuracy: "Weighted Accuracy",
            cls.NormMacroRecall: "Normed Macro Recall",
            cls.BalancedAccuracy: "Balanced Accuracy",
            cls.LogLoss: "Log Loss",
            cls.F1Macro: "Macro F1 Score",
            cls.F1Micro: "Micro F1 Score",
            cls.F1Weighted: "Weighted F1 Score",
            cls.PrecisionMacro: "Macro Precision",
            cls.PrecisionMicro: "Micro Precision",
            cls.PrecisionWeighted: "Weighted Precision",
            cls.RecallMacro: "Macro Recall",
            cls.RecallMicro: "Micro Recall",
            cls.RecallWeighted: "Weighted Recall",
            cls.AvgPrecisionMacro: "Macro Average Precision",
            cls.AvgPrecisionMicro: "Micro Average Precision",
            cls.AvgPrecisionWeighted: "Weighted Average Precision",
            cls.ExplainedVariance: "Explained Variance",
            cls.R2Score: "R2 Score",
            cls.Spearman: "Spearman Correlation",
            cls.MeanAbsError: "Mean Absolute Error",
            cls.MedianAbsError: "Median Absolute Error",
            cls.RMSE: "Root Mean Squared Error",
            cls.RMSLE: "Root Mean Squared Log Error",
            cls.NormMeanAbsError: "Normalized Mean Absolute Error",
            cls.NormMedianAbsError: "Normalized Median Absolute Error",
            cls.NormRMSE: "Normalized Root Mean Squared Error",
            cls.NormRMSLE: "Normalized Root Mean Squared Log Error",
            cls.MeanAveragePrecision: "Mean Average Precision (mAP)",
        }[metric]

    CLIPS_POS = {
        # TODO: If we are no longer transforming by default reconsider these
        # it is probably not necessary for them to be over 1
        LogLoss: 1,
        NormMeanAbsError: 1,
        NormMedianAbsError: 1,
        NormRMSE: 1,
        NormRMSLE: 1,
        # current timeout value but there is a long time
        TrainingResultsType.TRAIN_TIME: 10 * 60 * 2
    }

    CLIPS_NEG = {
        # TODO: If we are no longer transforming by default reconsider these
        # it is probably not necessary for them to be over 1
        # spearman is naturally limitted to this range but necessary for transform_y to work
        # otherwise spearmen is getting clipped to 0 by default
        Spearman: -1,
        ExplainedVariance: -1,
        R2Score: -1
    }


class MetricObjective:
    """Defines mappings from metrics to their objective.

    Objectives are maximization or minimization (regression and
    classification).
    """

    Classification = {
        Metric.AUCMicro: OptimizerObjectives.MAXIMIZE,
        Metric.AUCMacro: OptimizerObjectives.MAXIMIZE,
        Metric.AUCWeighted: OptimizerObjectives.MAXIMIZE,
        Metric.Accuracy: OptimizerObjectives.MAXIMIZE,
        Metric.WeightedAccuracy: OptimizerObjectives.MAXIMIZE,
        Metric.NormMacroRecall: OptimizerObjectives.MAXIMIZE,
        Metric.BalancedAccuracy: OptimizerObjectives.MAXIMIZE,
        Metric.LogLoss: OptimizerObjectives.MINIMIZE,
        Metric.F1Micro: OptimizerObjectives.MAXIMIZE,
        Metric.F1Macro: OptimizerObjectives.MAXIMIZE,
        Metric.F1Weighted: OptimizerObjectives.MAXIMIZE,
        Metric.PrecisionMacro: OptimizerObjectives.MAXIMIZE,
        Metric.PrecisionMicro: OptimizerObjectives.MAXIMIZE,
        Metric.PrecisionWeighted: OptimizerObjectives.MAXIMIZE,
        Metric.RecallMacro: OptimizerObjectives.MAXIMIZE,
        Metric.RecallMicro: OptimizerObjectives.MAXIMIZE,
        Metric.RecallWeighted: OptimizerObjectives.MAXIMIZE,
        Metric.AvgPrecisionMacro: OptimizerObjectives.MAXIMIZE,
        Metric.AvgPrecisionMicro: OptimizerObjectives.MAXIMIZE,
        Metric.AvgPrecisionWeighted: OptimizerObjectives.MAXIMIZE,
        Metric.MatthewsCorrelation: OptimizerObjectives.MAXIMIZE,
        Metric.AccuracyTable: OptimizerObjectives.NA,
        Metric.ConfusionMatrix: OptimizerObjectives.NA,
        TrainingResultsType.TRAIN_TIME: OptimizerObjectives.MINIMIZE
    }

    Regression = {
        Metric.ExplainedVariance: OptimizerObjectives.MAXIMIZE,
        Metric.R2Score: OptimizerObjectives.MAXIMIZE,
        Metric.Spearman: OptimizerObjectives.MAXIMIZE,
        Metric.MeanAbsError: OptimizerObjectives.MINIMIZE,
        Metric.NormMeanAbsError: OptimizerObjectives.MINIMIZE,
        Metric.MedianAbsError: OptimizerObjectives.MINIMIZE,
        Metric.NormMedianAbsError: OptimizerObjectives.MINIMIZE,
        Metric.RMSE: OptimizerObjectives.MINIMIZE,
        Metric.NormRMSE: OptimizerObjectives.MINIMIZE,
        Metric.RMSLE: OptimizerObjectives.MINIMIZE,
        Metric.NormRMSLE: OptimizerObjectives.MINIMIZE,
        Metric.MAPE: OptimizerObjectives.MINIMIZE,
        Metric.SMAPE: OptimizerObjectives.MINIMIZE,
        Metric.Residuals: OptimizerObjectives.NA,
        Metric.PredictedTrue: OptimizerObjectives.NA,
        TrainingResultsType.TRAIN_TIME: OptimizerObjectives.MINIMIZE
    }

    Forecast = {
        Metric.ForecastResiduals: OptimizerObjectives.NA,
        Metric.ForecastMAPE: OptimizerObjectives.NA,
        Metric.ForecastSMAPE: OptimizerObjectives.NA
    }

    ImageClassification = {
        Metric.Accuracy: OptimizerObjectives.MAXIMIZE,
    }

    ImageMultiLabelClassiciation = {
        Metric.Accuracy: OptimizerObjectives.MAXIMIZE,
    }

    ImageObjectDetection = {
        Metric.MeanAveragePrecision: OptimizerObjectives.MAXIMIZE,
    }


class ModelParameters:
    """
    Defines parameter names specific to certain models.

    For example, to indicate which features in the dataset are categorical
    a LightGBM model accepts the 'categorical_feature' parameter while
    a CatBoost model accepts the 'cat_features' parameter.
    """

    CATEGORICAL_FEATURES = {
        ModelClassNames.ClassificationModelClassNames.LightGBMClassifier: 'categorical_feature',
        ModelClassNames.RegressionModelClassNames.LightGBMRegressor: 'categorical_feature',
        ModelClassNames.ClassificationModelClassNames.CatBoostClassifier: 'cat_features',
        ModelClassNames.RegressionModelClassNames.CatBoostRegressor: 'cat_features'
    }


class TrainingType:
    """Defines validation methods.

    Different experiment types will use different validation methods.
    """

    # Yields TRAIN_FROM_FULL_METRICS and TEST_FROM_FULL_METRICS
    TrainFull = 'train_full'
    # Yields VALIDATION_METRICS
    TrainAndValidation = 'train_valid'
    # Yields TRAIN_METRICS, VALIDATION_METRICS, and TEST_METRICS
    TrainValidateTest = 'train_valid_test'
    # Yields CV_METRICS and CV_MEAN_METRICS
    CrossValidation = 'CV'
    MeanCrossValidation = 'MeanCrossValidation'
    FULL_SET = {
        TrainFull,
        TrainAndValidation,
        TrainValidateTest,
        CrossValidation,
        MeanCrossValidation}

    @classmethod
    def pretty(cls, metric):
        """Verbose names for training types."""
        return {
            cls.TrainFull: "Full",
            cls.TrainAndValidation: "Train and Validation",
            cls.CrossValidation: "Cross Validation",
            cls.MeanCrossValidation: "Mean of the Cross Validation",
        }[metric]


class NumericalDtype:
    """Defines supported numerical datatypes.

    Names correspond to the output of pandas.api.types.infer_dtype().
    """

    Integer = 'integer'
    Floating = 'floating'
    MixedIntegerFloat = 'mixed-integer-float'
    Decimal = 'decimal'

    FULL_SET = {Integer, Floating, MixedIntegerFloat, Decimal}


class DatetimeDtype:
    """Defines supported datetime datatypes.

    Names correspond to the output of pandas.api.types.infer_dtype().
    """

    Date = 'date'
    Datetime = 'datetime'
    Datetime64 = 'datetime64'

    FULL_SET = {Date, Datetime, Datetime64}


class TextOrCategoricalDtype:
    """Defines supported categorical datatypes."""

    String = 'string'
    Categorical = 'categorical'

    FULL_SET = {String, Categorical}


class TimeSeries:
    """Defines parameters used for timeseries."""

    TIME_COLUMN_NAME = 'time_column_name'
    GRAIN_COLUMN_NAMES = 'grain_column_names'
    GROUP_COLUMN_NAMES = 'group_column_names'
    DROP_COLUMN_NAMES = 'drop_column_names'
    GROUP_COLUMN = 'group'
    TARGET_LAGS = 'target_lags'
    FEATURE_LAGS = 'feature_lags'
    TARGET_ROLLING_WINDOW_SIZE = 'target_rolling_window_size'
    MAX_HORIZON = 'max_horizon'
    COUNTRY_OR_REGION = 'country_or_region'
    SEASONALITY = 'seasonality'
    USE_STL = 'use_stl'
    STL_OPTION_SEASON_TREND = 'season_trend'
    STL_OPTION_SEASON = 'season'
    SHORT_SERIES_HANDLING = 'short_series_handling'
    AUTO = 'auto'
    FREQUENCY = 'freq'
    MAX_CORES_PER_ITERATION = 'max_cores_per_iteration'


class TimeSeriesInternal:
    """Defines non user-facing TimeSeries constants."""

    DUMMY_GROUP_COLUMN = '_automl_dummy_group_col'
    DUMMY_ORDER_COLUMN = '_automl_original_order_col'
    DUMMY_GRAIN_COLUMN = '_automl_dummy_grain_col'
    DUMMY_TARGET_COLUMN = '_automl_target_col'
    DUMMY_PREDICT_COLUMN = '_automl_predict_col'
    MAX_HORIZON_FEATURIZER = 'max_horizon_featurizer'
    LAG_LEAD_OPERATOR = 'lag_lead_operator'
    ROLLING_WINDOW_OPERATOR = 'rolling_window_operator'
    ORIGIN_TIME_COLNAME = 'origin_time_column_name'
    MAKE_NUMERIC_NA_DUMMIES = 'make_numeric_na_dummies'
    IMPUTE_NA_NUMERIC_DATETIME = 'impute_na_numeric_datetime'
    MAKE_TIME_INDEX_FEATURES = 'make_time_index_featuers'
    DROP_IRRELEVANT_COLUMNS = 'drop_irrelevant_columns'
    MAKE_GRAIN_FEATURES = 'make_grain_features'
    MAKE_CATEGORICALS_NUMERIC = 'make_categoricals_numeric'
    MAKE_CATEGORICALS_ONEHOT = 'make_categoricals_onehot'
    MAKE_SEASONALITY_AND_TREND = 'make_seasonality_and_trend'
    RESTORE_DTYPES = 'restore_dtypes_transform'

    LAGS_TO_CONSTRUCT = 'lags'  # The internal lags dictionary
    WINDOW_SIZE = 'window_size'  # The internal window_size variable
    WINDOW_OPTS = 'window_options'  # The internal window options (Currently is not used).
    # The rolling window transform dictionary, currently not publicly available.
    TRANSFORM_DICT = 'transform_dictionary'
    TRANSFORM_OPTS = 'transform_options'  # The options for rolling window transform.
    DROP_NA = 'dropna'  # dropna parameter of LagLeadOperator and RollingWindow. Currently set to DROP_NA_DEFAULT.
    # overwrite_columns parameter of LagLeadOperator and RollingWindow. Currently set to OVERWRITE_COLUMNS_DEFAULT.
    OVERWRITE_COLUMNS = 'overwrite_columns'
    ORIGIN_TIME_COLUMN_NAME = 'origin_time_colname'
    ORIGIN_TIME_COLNAME_DEFAULT = 'origin'
    HORIZON_NAME = 'horizon_origin'
    MAX_HORIZON_DEFAULT = 1
    WINDOW_SIZE_DEFDAULT = 5
    TARGET_LAGS_DEFAULT = 1
    TRANSFORM_DICT_DEFAULT = {'min': DUMMY_TARGET_COLUMN,
                              'max': DUMMY_TARGET_COLUMN,
                              'mean': DUMMY_TARGET_COLUMN}
    DROP_NA_DEFAULT = True
    OVERWRITE_COLUMNS_DEFAULT = True
    # The amount of memory occupied by perspective data frame
    # at which we decide to switch off lag leads and rolling windows.
    MEMORY_FRACTION_FOR_DF = 0.7
    # The column name reserved for holiday feature
    HOLIDAY_COLUMN_NAME = '_Holiday'
    PAID_TIMEOFF_COLUMN_NAME = '_IsPaidTimeOff'

    SEASONALITY_VALUE_NONSEASONAL = 1
    SEASONALITY_VALUE_DETECT = -1
    SEASONALITY_VALUE_DEFAULT = SEASONALITY_VALUE_DETECT
    USE_STL_DEFAULT = None
    STL_VALID_OPTIONS = {TimeSeries.STL_OPTION_SEASON_TREND,
                         TimeSeries.STL_OPTION_SEASON}
    STL_SEASON_SUFFIX = '_season'
    STL_TREND_SUFFIX = '_trend'
    RESERVED_COLUMN_NAMES = {DUMMY_GROUP_COLUMN,
                             DUMMY_ORDER_COLUMN,
                             DUMMY_GRAIN_COLUMN,
                             DUMMY_TARGET_COLUMN}
    FORCE_TIME_INDEX_FEATURES_NAME = 'force_time_index_features'
    FORCE_TIME_INDEX_FEATURES_DEFAULT = None
    SHORT_SERIES_DROPPEER = "grain_dropper"
    SHORT_SERIES_HANDLING_DEFAULT = True
    CROSS_VALIDATIONS = 'n_cross_validations'
    TIMESERIES_PARAM_DICT = 'timeseries_param_dict'
    PROPHET_PARAM_DICT = 'prophet_param_dict'
    FEATURE_LAGS_DEFAULT = None
    RUN_TARGET_LAGS = 'forecasting_target_lags'
    RUN_WINDOW_SIZE = 'forecasting_target_rolling_window_size'
    RUN_MAX_HORIZON = 'forecasting_max_horizon'
    ARIMA_TRIGGER_CSS_TRAINING_LENGTH = 101


class Subtasks:
    """Defines names of the subtasks."""

    FORECASTING = 'forecasting'

    ALL = [FORECASTING]


class Transformers:
    """Defines transformers used for data processing."""

    X_TRANSFORMER = 'datatransformer'
    Y_TRANSFORMER = 'y_transformer'
    LAG_TRANSFORMER = 'laggingtransformer'
    TIMESERIES_TRANSFORMER = 'timeseriestransformer'
    ALL = [X_TRANSFORMER, Y_TRANSFORMER, LAG_TRANSFORMER, TIMESERIES_TRANSFORMER]


class TelemetryConstants:
    """Defines telemetry constants."""

    PRE_PROCESS_NAME = 'PreProcess'
    TRAINING_NAME = 'Training'
    FIT_ITERATION_NAME = 'FitIteration'
    OUTPUT_NAME = 'Output'
    GET_PIPELINE_NAME = 'GetPipeline'
    RUN_PIPELINE_NAME = 'RunPipeline'
    TIME_FIT_NAME = 'TimeFit'
    TIME_FIT_INPUT = 'TimeFitInput'
    RUN_TRAIN_VALID_NAME = 'TrainValid'
    RUN_TRAIN_FULL_NAME = 'TrainFull'
    RUN_CV_NAME = 'RunCV'
    RUN_CV_MEAN_NAME = 'RunCVMean'
    RUN_NAME = 'Run'
    COMPUTE_METRICS_NAME = 'ComputeMetrics'
    PREDICT_NAME = 'Predict'
    RUN_ENSEMBLING_NAME = 'RunEnsembling'
    DOWNLOAD_ENSEMBLING_MODELS = 'DownloadEnsemblingModels'
    TIME_FIT_ENSEMBLE_NAME = 'TimeFitEnsemble'
    METRIC_AND_SAVE_MODEL_NAME = 'MetricsAndSaveModel'
    ONNX_CONVERSION = 'ONNXConversion'
    MODEL_EXPLANATION = "ModelExplanation"
    COMPONENT_NAME = 'automl'
    SUCCESS = 'Success'
    FAILURE = 'Failure'
    GET_OUTPUT = 'GetOutput'
    GET_CHILDREN = 'GetChildren'
    REGISTER_MODEL = 'RegisterModel'
    DOWNLOAD_MODEL = 'DownloadModel'


def get_metric_from_type(t):
    """Get valid metrics for a given training type."""
    return {
        TrainingType.TrainFull: TrainingResultsType.TEST_FROM_FULL_METRICS,
        TrainingType.TrainAndValidation: (
            TrainingResultsType.VALIDATION_METRICS),
        TrainingType.TrainValidateTest: (
            TrainingResultsType.VALIDATION_METRICS),
        TrainingType.CrossValidation: TrainingResultsType.CV_MEAN_METRICS
    }[t]


def get_status_from_type(t):
    """Get valid training statuses for a given training type."""
    return {
        TrainingType.TrainFull: TrainingResultsType.TRAIN_FULL_STATUS,
        TrainingType.TrainAndValidation: (
            TrainingResultsType.TRAIN_VALIDATE_STATUS),
        TrainingType.TrainValidateTest: (
            TrainingResultsType.TRAIN_VALIDATE_STATUS),
        TrainingType.CrossValidation: TrainingResultsType.CV_STATUS
    }[t]


class ValidationLimitRule:
    """Defines validation rules."""

    def __init__(
        self,
        lower_bound: int,
        upper_bound: int,
        number_of_cv: int
    ):
        """Init the rule based on the inputs."""
        self.LOWER_BOUND = lower_bound
        self.UPPER_BOUND = upper_bound
        self.NUMBER_OF_CV = number_of_cv


class RuleBasedValidation:
    """Defines constants for the rule-based validation setting."""

    # Default CV number
    DEFAULT_N_CROSS_VALIDATIONS = 1  # is basically using train-validation split
    # Default train validate ratio
    DEFAULT_TRAIN_VALIDATE_TEST_SIZE = 0.1
    # Default train validate seed
    DEFAULT_TRAIN_VALIDATE_RANDOM_STATE = 42

    VALIDATION_LIMITS_NO_SPARSE = [
        ValidationLimitRule(0, 1000, 10),
        ValidationLimitRule(1000, 20000, 3),
        ValidationLimitRule(20000, sys.maxsize, 1)
    ]

    SPARSE_N_CROSS_VALIDATIONS = 1  # sparse is basically using train-validation split


# Hashing seed value for murmurhash
hashing_seed_value = 314489979


# Default app_name in custom dimensions of the logs.
DEFAULT_LOGGING_APP_NAME = "AutoML"
LOW_MEMORY_THRESHOLD = 0.5


class FeatureSweeping:
    """Defines constants for Feature Sweeping."""

    LOGGER_KEY = 'logger'


class AutoMLJson:
    """Defines constants for JSON created by automated ML."""

    SCHEMA_TYPE_FAULT_VERIFIER = 'fault_verifier'


class AutoMLValidation:
    TIMEOUT_DATA_BOUND = 10000000


class CheckImbalance:
    """
    If the ratio of the samples in the minority class to the samples in the majority class
    is equal to or lower than this threshold, then Imbalance will be detected in the dataset.
    """
    MINORITY_TO_MAJORITY_THRESHOLD_RATIO = 0.2
