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

### Statistics

```python
# single metrics
metrics = dm.Metrics('metrics/run1.0')
metrics.read('loss') # pd.Series

# comparing runs
runs = { run: dm.Metrics(run) for run in ['metrics/version1', 'metrics/version2'] }
df = dm.compare(runs, 'loss') # pd.DataFrame with columns ("run1.0", "run1.1", ...)

# concatenating runs (i.e. they're the same experiment but trained by steps or something)
runs = [dm.Metrics(run) for run in ['metrics/part1', 'metrics/part2']]
df = dm.concat(runs, 'loss') # pd.Series with cumulative step indices
```