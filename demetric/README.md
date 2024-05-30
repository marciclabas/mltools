# Demetric

> Simple and composable metric tracking and logging for ML

```python
import demetric as dm

run = dm.Run(id='gpt2-3', base_path='runs', meta={
  'model': 'gpt2',
  'batch_size': 128
})

run.log('loss', value=loss, step=step)
run.log('accuracy', value=acc, step=step)


fig, ax = run.plot('loss')
fig2, ax2 = run.plot_summary()
```


Creates:

```
runs/
  gpt2-3/
    meta.json
    metrics/
      loss.csv
      accuracy.csv
```