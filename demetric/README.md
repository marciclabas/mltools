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
runs = dm.runs('metrics/run1.*')
df = dm.compare(runs, 'loss') # pd.DataFrame with columns ("run1.0", "run1.1", ...)

# concatenating runs (i.e. they're the same experiment but trained by steps or something)
df = dm.concat(runs, 'loss') # pd.Series with cumulative step indices

# whatever you want to do with the pd.Series's
ss = dm.readall(runs, 'loss') # list[pd.Series] with `metrics.id` as each name
```