define([], function() {

    const SettingModel = class {
        static mInstance = null;

        mBaseDirStr = '';
        
        constructor(){
            if(!this.mInstance){
                this.mInstance = this;
            } 
            return this.mInstance;
        }

        static GetInstance = () => {
            return this;
        }

        GetBaseDirStr = () => {
            return this.mBaseDirStr;
        }

        SetBaseDirStr = (baseDirStr) => {
            this.mBaseDirStr = baseDirStr;
        }

    }

    return new SettingModel();
});