import uno
  
def connect():
    try:
        localctx = uno.getComponentContext()
        resolver = localctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver",localctx)
        ctx = resolver.resolve(
           "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    except:
        return None
    return ctx
  
  
def mri(ctx, target):
    mri = ctx.ServiceManager.createInstanceWithContext(
        "mytools.Mri",ctx)
    mri.inspect(target)

if __name__=="__main__":
    ctx = connect()
    if ctx == None:
        print ("Failed to connect.")
        import sys
        sys.exit()
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop",ctx)
    model = desktop.loadComponentFromURL("private:factory/swriter","_default",0,())
    mri(ctx,model)
    ctx.ServiceManager
