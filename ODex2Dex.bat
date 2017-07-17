cd %~dp1
del /s/f/q out
java -jar baksmali.jar -d system/framework -x %~1
java -jar smali.jar -o %~n1_classes.dex out