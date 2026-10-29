pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
    }

    parameters {
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Browser to run on')
        string(name: 'MARKERS', defaultValue: 'sanity or regression', description: 'Pytest marker expression')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/shamnitjsr/opencartPlaywrightPythonFramework.git'
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    def browser = params.BROWSER
                    bat """
                    "C:/Users/SHAMBHU KUMAR/AppData/Local/Programs/Python/Python314/python.exe" -m venv .venv
                    .venv/Scripts/python.exe -m pip install --upgrade pip
                    .venv/Scripts/python.exe -m pip install -r requirements.txt
                    .venv/Scripts/python.exe -m playwright install ${browser}
                    """
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def browser = params.BROWSER
                    def markers = params.MARKERS
                    bat """
                    .venv/Scripts/python.exe -m pytest tests -m "${markers}" --browser=${browser} --junitxml=reports/junit.xml
                    """
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
    }
}