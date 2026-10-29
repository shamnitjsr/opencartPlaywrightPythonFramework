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
                    // credentialsId: 'github-creds'   // uncomment for a private repo
            }
        }

        stage('Setup Environment') {
            steps {
                bat '''
                "C:\\Users\\SHAMBHU KUMAR\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" -m venv .venv
                call .venv\\Scripts\\activate.bat
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                playwright install chromium firefox webkit
                '''
    }
}

        stage('Run Tests') {
            steps {
                bat """
                call .venv\\Scripts\\activate.bat
                pytest tests -m "${params.MARKERS}" --browser=${params.BROWSER} --junitxml=reports/junit.xml
                """
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            allure includeProperties: false, jdk: '', results: [[path: 'reports/allure-results']]
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            publishHTML(target: [
                reportDir: 'reports',
                reportFiles: 'myreport.html',
                reportName: 'Pytest HTML Report',
                keepAll: true,
                allowMissing: true,
                alwaysLinkToLastBuild: true
            ])
        }
    }
}