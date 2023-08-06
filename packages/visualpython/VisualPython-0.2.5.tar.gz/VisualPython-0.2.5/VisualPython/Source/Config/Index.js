define([], function() {

    /*
        개발모드와 프로덕션모드를 구분하는게 좋다고 해서 만든 config입니다.

        0은 development mode 개발 모드
        1은 production mode 프로덕션 모드
    */
    const PROCESS_MODE = 0;
    const AWS_S3_CSVDATA_URL = "https://visual-python-csv-data.s3.ap-northeast-2.amazonaws.com";
    return {
        PROCESS_MODE,
        AWS_S3_CSVDATA_URL
    }
});