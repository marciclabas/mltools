# Demetric

> Dead simple standard for metric logging

### Logging

```python
import demetric as dm

metrics = dm.Metrics.new('metrics/gpt2-3')

metrics.log('loss', value=loss, step=step)
metrics.log('accuracy', value=acc, step=step)
# ...
```


Creates:

```
runs/
  gpt2-3/
    loss.csv
    accuracy.csv
```

### Reading

```python
# single metrics
metrics = dm.Metrics('metrics/run1.0')
metrics.read('loss') # pd.DataFrame

# all metrics
metrics.read() # pd.DataFrame with a column per metric

# comparing runs
runs = { run: dm.Metrics(run) for run in ['metrics/version1', 'metrics/version2'] }
df = dm.compare(runs, 'loss') # pd.DataFrame with columns ("loss_run1.0", "loss_run1.1", ...)

# concatenating runs (i.e. they're the same experiment but trained by steps or something)
runs = [dm.Metrics(run) for run in ['metrics/part1', 'metrics/part2']]
df = dm.concat(runs, 'loss') # pd.DataFrame with cumulative step indices
```