import numpy as np
from catboost import CatBoostClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import onnx
from onnxruntime import InferenceSession

X, y = make_classification(n_samples=100, n_features=4, random_state=42)
X = np.array(X, dtype=np.float32)
y = np.array(y, dtype=np.int32)

# Define and train the pipeline
pipeline = Pipeline(
    [
        ("scaler", StandardScaler()),
    ]
)

pipeline.fit(X, y)

fitted_values = pipeline.transform(X)

catboost_model = CatBoostClassifier()
catboost_model.fit(fitted_values, y)

catboost_model.save_model("model.onnx", format="onnx")

initial_types = [("float_input", FloatTensorType([None, X.shape[1]]))]
onnx_preprocessing_model = convert_sklearn(
    pipeline.named_steps["scaler"], initial_types=initial_types
)

onnx.save_model(onnx_preprocessing_model, "preprocessing_pipeline.onnx")

print("ONNX preprocessing model saved as 'preprocessing_pipeline.onnx'")
