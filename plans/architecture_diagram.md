# OCR Document Categorizer - System Architecture

## Component Diagram

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[React UI] --> B[Upload Component]
        A --> C[Results Display]
        A --> D[Camera Capture]
    end
    
    subgraph "Backend Services"
        E[FastAPI Server] --> F[Document Processor]
        E --> G[OCR Handler]
        E --> H[Text Categorizer]
    end
    
    subgraph "External Libraries"
        I[OpenCV] --> F
        J[Tesseract] --> G
        K[Pillow] --> F
        K --> G
    end
    
    subgraph "Data Flow"
        B --> E
        F --> G
        G --> H
        H --> C
    end
    
    style A fill:#e1f5fe
    style E fill:#f3e5f5
    style I fill:#e8f5e8
    style J fill:#fff3e0
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant BE as Backend
    participant DD as Document Detector
    participant OCR as OCR Engine
    participant TC as Text Categorizer
    
    U->>FE: Upload document image
    FE->>BE: POST /upload with image
    BE->>DD: Detect document boundaries
    DD-->>BE: Return document contour
    BE->>BE: Crop document image
    BE->>OCR: Extract text from cropped image
    OCR-->>BE: Return extracted text
    BE->>TC: Categorize text
    TC-->>BE: Return categorized data
    BE-->>FE: Return categorized results
    FE-->>U: Display structured results
```

## File Organization

```mermaid
graph TD
    subgraph "Project Root"
        PR[Project-OCR]
    end
    
    subgraph "Backend"
        BA[backend/]
        BB[main.py]
        BC[document_processor.py]
        BD[ocr_handler.py]
        BE[text_categorizer.py]
        BF[requirements.txt]
    end
    
    subgraph "Frontend"
        FA[frontend/]
        FB[src/]
        FC[components/]
        FD[pages/]
        FE[App.jsx]
        FF[package.json]
    end
    
    subgraph "Documentation"
        DA[plans/]
        DB[project_plan.md]
        DC[technical_spec.md]
        DD[roadmap.md]
        DE[architecture_diagram.md]
    end
    
    PR --> BA
    PR --> FA
    PR --> DA
    BA --> BB
    BA --> BC
    BA --> BD
    BA --> BE
    BA --> BF
    FA --> FB
    FA --> FC
    FA --> FD
    FA --> FE
    FA --> FF
    DA --> DB
    DA --> DC
    DA --> DD
    DA --> DE
```

## API Flow

```mermaid
flowchart LR
    A[Image Upload] --> B[Validate File Type]
    B --> C[Save Temp File]
    C --> D[Load Image]
    D --> E[Detect Document Contour]
    E --> F[Crop Document]
    F --> G[Preprocess for OCR]
    G --> H[Extract Text with Tesseract]
    H --> I[Categorize Text]
    I --> J[Format Response]
    J --> K[Return JSON Result]
    K --> L[Clean Up Temp Files]
    
    E -->|No document found| M[Use Full Image]
    M --> G