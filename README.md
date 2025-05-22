# Pharmaceutical Supply Security Platform

A comprehensive platform for managing and securing pharmaceutical supply chains, with a focus on cold chain compliance, medical device sterilization, economic modeling, and risk assessment.

## Features

### Cold Chain Management
- **Temperature Monitoring**
  - Real-time temperature tracking
  - Automated alerts for deviations
  - Historical data analysis
  - Compliance reporting
- **Facility Management**
  - Multi-location support
  - Capacity planning
  - Certification tracking
  - Maintenance scheduling
- **Incident Management**
  - Incident tracking and reporting
  - Root cause analysis
  - Corrective action planning
  - Preventive measure implementation

### Medical Device Sterilization
- **Batch Processing**
  - Batch tracking and tracing
  - Quality control parameters
  - Release management
  - Documentation
- **Facility Management**
  - Capacity utilization
  - Equipment maintenance
  - Certification compliance
  - Emission control monitoring
- **Quality Assurance**
  - Quality check procedures
  - Compliance verification
  - Documentation management
  - Audit trail

### Economic Analysis
- **Cost Analysis**
  - Capital expenditure tracking
  - Operational cost management
  - Maintenance cost analysis
  - Cost optimization
- **Benefit Analysis**
  - Revenue tracking
  - Cost savings calculation
  - Efficiency improvements
  - ROI analysis
- **Risk Assessment**
  - Market risk evaluation
  - Operational risk analysis
  - Regulatory compliance costs
  - Contingency planning

### Risk Assessment
- **Risk Identification**
  - Risk factor cataloging
  - Impact assessment
  - Probability analysis
  - Dependency mapping
- **Mitigation Planning**
  - Strategy development
  - Implementation tracking
  - Effectiveness monitoring
  - Cost-benefit analysis
- **Monitoring & Reporting**
  - Key performance indicators
  - Compliance metrics
  - Trend analysis
  - Alert management

## Technical Architecture

### Backend
- FastAPI for high-performance API
- SQLAlchemy ORM for database operations
- PostgreSQL for data storage
- Alembic for database migrations
- Pydantic for data validation

### Frontend (Planned)
- React for user interface
- Material-UI for components
- Chart.js for data visualization
- Redux for state management

### Infrastructure
- Docker for containerization
- Docker Compose for orchestration
- GitHub Actions for CI/CD
- AWS for cloud deployment (planned)

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Docker and Docker Compose
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/deluair/Pharmaceutical-Supply-Security-Platform.git
cd Pharmaceutical-Supply-Security-Platform
```

2. Create and activate a virtual environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Database Setup

1. Start the PostgreSQL database:
```bash
docker-compose up -d db
```

2. Run database migrations:
```bash
# On Windows
python -m alembic upgrade head

# On Linux/Mac
./scripts/run_migrations.sh
```

3. Generate sample data:
```bash
# On Windows
python scripts/generate_sample_data.py

# On Linux/Mac
./scripts/run_sample_data.sh
```

## Running the Application

1. Start the application:
```bash
docker-compose up -d
```

2. Access the API documentation:
```
http://localhost:8000/docs
```

## Development

### Project Structure

```
pharmaceutical-supply-security-platform/
├── alembic/                  # Database migrations
├── app/
│   ├── api/                  # API endpoints
│   │   ├── v1/              # API version 1
│   │   └── deps.py          # API dependencies
│   ├── core/                # Core functionality
│   │   ├── config.py        # Configuration
│   │   └── security.py      # Security utilities
│   ├── models/              # Database models
│   │   ├── cold_chain.py    # Cold chain models
│   │   ├── sterilization.py # Sterilization models
│   │   ├── economic.py      # Economic models
│   │   └── risk.py          # Risk assessment models
│   └── services/            # Business logic
├── scripts/                 # Utility scripts
│   ├── run_migrations.sh    # Migration script
│   └── generate_sample_data.py # Sample data generator
├── tests/                   # Test suite
├── .env.example            # Example environment variables
├── docker-compose.yml      # Docker configuration
├── Dockerfile              # Docker build file
└── requirements.txt        # Python dependencies
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_cold_chain.py

# Run with coverage
pytest --cov=app tests/
```

### Code Style

The project follows PEP 8 style guidelines. To check your code:

```bash
# Run flake8
flake8

# Run black for formatting
black .

# Run isort for import sorting
isort .
```

## API Documentation

The API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

#### Cold Chain Management
- `GET /api/v1/cold-chain/facilities` - List facilities
- `POST /api/v1/cold-chain/facilities` - Create facility
- `GET /api/v1/cold-chain/temperature-logs` - Get temperature logs
- `POST /api/v1/cold-chain/incidents` - Report incident

#### Sterilization
- `GET /api/v1/sterilization/facilities` - List facilities
- `POST /api/v1/sterilization/batches` - Create batch
- `GET /api/v1/sterilization/quality-checks` - Get quality checks
- `POST /api/v1/sterilization/incidents` - Report incident

#### Economic Analysis
- `GET /api/v1/economic/analyses` - List analyses
- `POST /api/v1/economic/costs` - Add cost item
- `GET /api/v1/economic/benefits` - List benefits
- `POST /api/v1/economic/risk-factors` - Add risk factor

#### Risk Assessment
- `GET /api/v1/risk/assessments` - List assessments
- `POST /api/v1/risk/factors` - Add risk factor
- `GET /api/v1/risk/mitigations` - List mitigations
- `POST /api/v1/risk/metrics` - Add monitoring metric

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Development Workflow

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit:
```bash
git add .
git commit -m "Description of your changes"
```

3. Push to your fork:
```bash
git push origin feature/your-feature-name
```

4. Create a Pull Request on GitHub

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please:
1. Check the [documentation](docs/)
2. Open an issue in the GitHub repository
3. Contact the development team

## Roadmap

### Phase 1 (Current)
- [x] Basic API structure
- [x] Database models
- [x] Core functionality
- [x] Sample data generation

### Phase 2 (Next)
- [ ] Frontend development
- [ ] Advanced analytics
- [ ] Real-time monitoring
- [ ] User authentication

### Phase 3 (Future)
- [ ] Mobile application
- [ ] Machine learning integration
- [ ] Blockchain integration
- [ ] Advanced reporting 