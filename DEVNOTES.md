#  Release Notes

We build the web ui and check it in, this way users do not need to build it themselves after starting the python applicaiton, we may change this as we switch to a distribution of the .exe file instead of the source code.

## To build the web ui

```bash
cd open-gateway/webui
yarn build
```

## To build the python application

```bash
    cd open-gateway
    python -m PyInstaller .\app.spec --onefile
```

this will create an .exe file in the dist folder

