define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/PaletteElement`,
], function( 
    FrontEndApis
 ){
    const { SetCodeAndExecute } = FrontEndApis.JupyterNativeApi;
    const BaseLibrary = class extends PaletteElement {
        static mInstance = null;
        mName = "BaseLibrary";
        
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
            let str = `# Import Standard libraries\n\nimport pandas as pd\nimport numpy as np\n\n`;
             
            str += `from sklearn import datasets, linear_model\n`;
            str += `from sklearn.metrics import mean_squared_error, r2_score\n`;
         
            str += `from sklearn.pipeline import make_pipeline\n`;
            str += `from sklearn.preprocessing import StandardScaler\n`;
            str += `from sklearn.neighbors import KNeighborsClassifier\n\n`;
                        
            str += `import matplotlib.pyplot as plt\n`;
         
            SetCodeAndExecute(str);
        }
    }
    
    return new BaseLibrary();
});
