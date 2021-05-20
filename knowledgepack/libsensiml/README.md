### Running a knowledge pack on the gateway

In some cases you may want to run a Knowledge Pack on the gateway itself. This is currently possible by turning the Knowledge Pack into a shared object file. Download a Knowledge Pack library for your gateway's platform. Unzip the folder and go to the libsensiml directory. Here you will see a libsensiml.a file. You need to convert this to a shared object by running the following.

```bash
ar -x libsensiml.a
gcc -shared -o libsensiml.so *.o
```

copy the libsensiml.so file to this folder open-gateway/knowledgepack/libsensiml folder. It will automatically be used when you launch the gateway
