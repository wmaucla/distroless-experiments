from onnxruntime import InferenceSession
import numpy as np

onnx_preprocessing_model_path = "preprocessing_pipeline.onnx"
onnx_session = InferenceSession(onnx_preprocessing_model_path)

X_test = np.array([[0.5, -1.2, 1.5, 0.3]], dtype=np.float32)

preprocessed_input = onnx_session.run(
    None, {onnx_session.get_inputs()[0].name: X_test}
)[0]

# Apply CatBoost model
sess = InferenceSession("model.onnx")

predictions = sess.run(["probabilities"], {"features": preprocessed_input})

print("Inference results:", predictions)
