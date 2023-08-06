define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/PaletteElement`,
], function( 
    FrontEndApis
 ){
    const { SetCodeAndExecute } = FrontEndApis.JupyterNativeApi;
    const PdDataFrame = class extends PaletteElement {
        static mInstance = null;
        mName = "PdDataFrame";
        
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
            let str = `data = {'year': [2018, 2019, 2020],'GDP rate': [2.8, 3.1, 3.0],'GDP': ['1.637M', '1.73M', '1.83M']}\n`;
            str += `df = pd.DataFrame(data)\n`;
            str += `df`;

            SetCodeAndExecute(str);
        }
    }
    
    return new PdDataFrame();
});
