define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/PaletteElement`,
], function( 
    FrontEndApis
 ){
    const { SetCodeAndExecute } = FrontEndApis.JupyterNativeApi;
    const NpRavel = class extends PaletteElement {
        static mInstance = null;
        mName = "NpRavel";
        
        constructor(){
            super();
            if(!this.mInstance){
                this.mInstance = this;
            } 
            return this.mInstance;
        }

        static GetInstance = () => {
            return this.mInstance;
        }

        GetName = () => {
            return this.mName;
        }

        ExecuteCode = () => {
            let str = `arr = np.array( [ (3,2,4,1),(1,7,3,4) ] )\n`;
            str += `print(arr)`;
            SetCodeAndExecute(str);
            
            str = ``;
            str += `arr2 = arr.ravel()\n`;
            str += `print(arr2)`;
            SetCodeAndExecute(str);
        }
    }
    
    return new NpRavel();
});
