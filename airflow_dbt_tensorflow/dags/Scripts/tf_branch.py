import pandas as pd
import tensorflow as tf
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from io import StringIO
import os
import numpy as np
import logging

def tensorflow_branch(keys):
    # Configure environment for stability
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Completely disable GPU
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'   # Suppress all TensorFlow logs
    tf.get_logger().setLevel('ERROR')
    tf.autograph.set_verbosity(0)
    np.random.seed(42)  # For reproducibility
    
    print("Running TensorFlow script with keys:", keys)
    
    s3_hook = S3Hook(aws_conn_id='awsID')
    bucket_name = 'rabbitmq-reddit'

    for key in keys:
        print(f"Downloading {key} from S3")
        obj = s3_hook.get_key(bucket_name=bucket_name, key=key)
        csv_content = obj.get()['Body'].read().decode('utf-8')

        # Load and prepare data
        df = pd.read_csv(StringIO(csv_content))
        print(f"Data shape: {df.shape}")

        # Configure target and features
        TARGET_COL = 'score'
        FEATURE_COL = 'num_comments'  # Explicitly select feature
        
        if TARGET_COL not in df.columns:
            raise ValueError(f"Expected column '{TARGET_COL}' not found")
        if FEATURE_COL not in df.columns:
            raise ValueError(f"Feature column '{FEATURE_COL}' not found")

        # Prepare data
        X = df[[FEATURE_COL]].fillna(0).values
        y = df[TARGET_COL].values
        
        # Normalize features
        X_mean, X_std = X.mean(), X.std()
        if X_std == 0:  # Handle constant features
            X_std = 1
        X = (X - X_mean) / X_std
        
        print(f"\n{'='*50}")
        print(f"Training Details for {key}")
        print(f"{'='*50}")
        print(f"Samples: {len(X)}")
        print(f"Feature: {FEATURE_COL}")
        print(f"Target: {TARGET_COL}")
        print(f"Feature mean: {X_mean:.2f}, std: {X_std:.2f}")
        print(f"Target range: {y.min()}-{y.max()}")
        print(f"{'='*50}\n")

        # Create simple linear regression model
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(1,)),
            tf.keras.layers.Dense(1)  # Single neuron for linear regression
        ])
        
        # Custom callback for better logging
        class TrainingLogger(tf.keras.callbacks.Callback):
            def on_epoch_end(self, epoch, logs=None):
                print(f"Epoch {epoch+1}: loss={logs['loss']:.4f}")

        # Configure model
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.1),
            loss='mse'
        )
        
        print("Model architecture:")
        model.summary()
        print("\nStarting training...")

        # Train model
        history = model.fit(
            X, y,
            epochs=10,
            verbose=0,
            batch_size=4,
            callbacks=[TrainingLogger()]
        )

        # Evaluate
        final_loss = history.history['loss'][-1]
        print(f"\nTraining complete! Final loss: {final_loss:.4f}")
        
        # Save model
        model_path = f"/tmp/{key.split('.')[0]}_model.keras"
        model.save(model_path)
        print(f"Model saved to {model_path}")
        print(f"{'='*50}\n")

        print(f"Finished processing {key}")