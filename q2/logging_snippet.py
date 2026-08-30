mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("mnist-mlp")

with mlflow.start_run(run_name=run_name) as run:

    mlflow.log_params({
        "model_type": "MLPClassifier",
        "dataset": "MNIST",
        "hidden_layer_sizes": str(hidden_layer_sizes),
        "learning_rate_init": learning_rate_init,
        "batch_size": batch_size,
        "alpha": alpha,
        "epochs": epochs,
        "solver": "adam",
        "activation": "relu",
        "subsample": SUBSAMPLE,
        "seed": SEED,
    })

    mlflow.set_tag("team", "data-science")
    mlflow.set_tag("assignment", "module1-q2")

    for epoch in range(epochs):
        model.fit(X_train, y_train)

        train_loss = model.loss_
        val_proba = model.predict_proba(X_test)
        val_acc = accuracy_score(y_test, np.argmax(val_proba, axis=1))
        val_loss = log_loss(y_test, val_proba, labels=np.arange(10))
        train_acc = accuracy_score(y_train, model.predict(X_train))

        mlflow.log_metric("train_loss", train_loss, step=epoch)
        mlflow.log_metric("val_accuracy", val_acc, step=epoch)
        mlflow.log_metric("val_loss", val_loss, step=epoch)
        mlflow.log_metric("train_accuracy", train_acc, step=epoch)
        mlflow.log_metric("generalization_gap", train_acc - val_acc, step=epoch)

    preds = model.predict(X_test)
    mlflow.log_metrics({
        "final_val_accuracy": accuracy_score(y_test, preds),
        "final_f1_macro": f1_score(y_test, preds, average="macro"),
        "final_train_loss": model.loss_,
        "best_val_accuracy": best_acc,
        "best_epoch": best_epoch,
        "train_time_sec": elapsed,
    })

    mlflow.log_artifact("loss_curve.csv")

    signature = infer_signature(X_test[:5], model.predict(X_test[:5]))
    mlflow.sklearn.log_model(
        model,
        name="model",
        signature=signature,
        input_example=X_test[:5],
        serialization_format="cloudpickle",
    )
