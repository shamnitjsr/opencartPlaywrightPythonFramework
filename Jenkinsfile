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
                    def pythonPath = "C:\\Users\\SHAMBHU KUMAR\\AppData\\Local\\Programs\\Python\\Python314\\python.exe"
                    def browserName = params.BROWSER ? params.BROWSER : 'chromium'

                    bat """
                        "${pythonPath}" -m venv .venv
                        .venv\\Scripts\\python.exe -m pip install --upgrade pip
                        .venv\\Scripts\\python.exe -m pip install -r requirements.txt
                        .venv\\Scripts\\python.exe -m playwright install ${browserName}
                    """
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def markers = params.MARKERS ? params.MARKERS : 'sanity or regression'

                    bat """
                        .venv\\Scripts\\python.exe -m pytest tests -m "${markers}" --junitxml=reports/junit.xml
                    """
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true

            allure includeProperties: false,
                   jdk: '',
                   results: [[path: 'reports/allure-results']],
                   commandLine: 'allure'
        }
    }
}