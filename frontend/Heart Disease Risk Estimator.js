function toggleMenu() {
    const menu = document.querySelector(".menu-links");
    const icon = document.querySelector(".hamburger-icon");
    menu.classList.toggle("open");
    icon.classList.toggle("open");
  }

  async function handleSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    // Map form values to model input order and encoding
    const featureOrder = [
      'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
      'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
    ];
    // Encoding maps
    const sexMap = { 'male': 1, 'female': 0 };
    const cpMap = {
      'typical angina': 1,
      'atypical angina': 2,
      'non-anginal': 3,
      'asymptomatic': 0
    };
    const fbsMap = { 'true': 1, 'false': 0 };
    const restecgMap = {
      'normal': 0,
      'stt abnormality': 1,
      'iv hypertrophy': 2
    };
    const exangMap = { 'true': 1, 'false': 0 };
    const thalMap = {
      'normal': 1,
      'fixed defect': 2,
      'reversible defect': 3
    };
    // Prepare features array
    const data = {};
    formData.forEach((value, key) => { data[key] = value; });
    const features = [
      Number(data.age),
      sexMap[data.sex],
      cpMap[data.cp],
      Number(data.trestbps),
      Number(data.chol),
      fbsMap[data.fbs],
      restecgMap[data.restecg],
      Number(data.thalach),
      exangMap[data.exang],
      Number(data.oldpeak),
      Number(data.slope),
      Number(data.ca),
      thalMap[data.thal]
    ];
    // Call backend API
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ features })
    });
    const result = await response.json();
    // Redirect to results page with risk info
    const params = new URLSearchParams({
      ...data,
      risk_percent: result.risk_percent,
      risk_level: result.risk_level
    });
    window.location.href = `Heart Beat Results.html?${params.toString()}`;
  }

  document.getElementById('predictionForm').onsubmit = handleSubmit;