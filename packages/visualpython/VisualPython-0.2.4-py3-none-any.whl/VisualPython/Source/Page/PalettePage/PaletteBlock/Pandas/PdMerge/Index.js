define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/PaletteElement`,
], function( 
    FrontEndApis
 ){
    const { SetCodeAndExecute } = FrontEndApis.JupyterNativeApi;
    const PdMerge = class extends PaletteElement {
        static mInstance = null;
        mName = "PdMerge";
        
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
            let str = `df = pd.DataFrame({'Week': ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7'], 'A': [34, 67, 92, 31, 90, 100, 101]})\n`;
            str += `df2 = pd.DataFrame({'Week': ['W4', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10'], 'B': [75, np.nan, 53, 21, 94, 47, 88]})\n`;
            str += `df3 = pd.DataFrame({'Week': ['W12', 'W13', 'W14', 'W15', 'W16', 'W17', 'W18'], 'C': [25, 30, 40, 45, 46, 47, 48]})\n`;
            str += `df = pd.merge(df, df2, on='Week', how='left')\n`;
            str += `df`;
            SetCodeAndExecute(str);

            str = ``;
            str += `df = pd.merge(df, df3, on='Week', how='left')\n`;
            str += `df`;
            SetCodeAndExecute(str);
        }
    }
    
    return new PdMerge();
});
