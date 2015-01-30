# TraceDisplay
Python tool to generate simple charts of calls of spinlocks from logs of Ftrace

## Usage
You must have captured the log of Ftrace with the function-graph option and displaying the timestamp in each record. To do this, configure Ftrace with:
```bash
echo /sys/kernel/debug/tracing/duration-proc > trace_options
```
Enable the function graph as current tracer
```bash
echo function_graph > /sys/kernel/debug/tracing/current_tracer
```

enable the tracer and run your tests. Finally, use the result log -avaliable in the directory of Ftrace- and use the script as
```bash
cp /sys/kernel/debug/tracing/trace data.txt
python SpinLockTracer.py data.txt
```
passing as argument the source file of data generated with Ftrace.

## Result
The final result generate a window of TKinter displaying the full records with colors and a caption that can be recorded.

![](https://raw.githubusercontent.com/sebablasko/TraceDisplay/master/resultExample.png)
