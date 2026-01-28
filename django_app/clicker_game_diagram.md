# Clicker Game System Architecture

## Component Diagram

```mermaid
graph TD
    A[Client Frontend] --> B[API Gateway]
    B --> C[Django REST API]
    C --> D[(PostgreSQL Database)]
    C --> E[(Redis Cache)]
    C --> F[Celery Workers]
    F --> D
    F --> E
    G[Telegram API] --> B
    H[Admin Panel] --> C
    
    subgraph Backend
        C
        D
        E
        F
    end
    
    subgraph External Services
        G
        H
    end
    
    subgraph Client
        A
    end
```

## Data Flow Diagram

```mermaid
graph LR
    A[Player] --> B[Click Action]
    B --> C[Client Validation]
    C --> D[Energy Update]
    D --> E[Balance Update]
    E --> F[State Sync]
    F --> G[Server Validation]
    G --> H[Database Update]
    H --> I[Cache Update]
    
    J[Background Tasks] --> H
    J --> I
    
    K[API Requests] --> G
    K --> I
```

## Player Lifecycle

```mermaid
graph TD
    A[Player Registration] --> B[Profile Creation]
    B --> C[Initial State Setup]
    C --> D[Gameplay]
    D --> E[Clicking]
    D --> F[Purchasing Upgrades]
    D --> G[Claiming Rewards]
    D --> H[Completing Tasks]
    E --> I[Energy Management]
    F --> J[State Updates]
    G --> J
    H --> J
    J --> K[Sync with Server]
    K --> L[Validation]
    L --> M[Database Update]
    M --> N[Continue Gameplay]
    
    O[Background Tasks] --> M