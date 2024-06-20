## On the fly checking

If you want to get a quick look at the xs (example executable):

```
python doXsCalcOnFly.py -j testReport_hexa48_2023-08-05_15-01-21.json --target ECOND -p 8.94e+12 
```

Give it an output, and it will give you the xs for the largest block. Additional command line options allow you to combine all blocks (`-all True`) or if you have access to several runs on the same hexacontroller, combine them together for the largest block (`-combo True`)
