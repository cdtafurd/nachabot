
# 🤖 Nachabot - Asistente de Admisiones UNAL

Nachabot es un chatbot inteligente desarrollado para asistir a aspirantes de pregrado en el proceso de admisión a la Universidad Nacional de Colombia. Utiliza un enfoque de **Generación Aumentada por Recuperación (RAG)** implementado con **LangChain**, **LangGraph** y desplegado como aplicación web usando **Streamlit**.

🔗 Accede a la aplicación aquí: [https://nachabot-dev.streamlit.app/](https://nachabot-dev.streamlit.app/)

---

## 🧠 ¿Qué hace Nachabot?

Nachabot responde preguntas relacionadas con:

- Fechas clave de inscripción y pruebas
- Requisitos para aspirantes especiales (PAES, PEAMA, PAET)
- Procedimientos de selección y admisión
- Normativa vigente y guías oficiales

Se alimenta de documentos extraídos del sitio web oficial de admisiones de la UNAL y de PDFs institucionales, procesados mediante scraping y carga de archivos.

---

## ⚙️ Arquitectura

- **RAG (Retrieval-Augmented Generation)** con LangChain
- **LangGraph** para flujos conversacionales y gestión de herramientas
- **OpenAI / Ollama** como backends de LLMs (intercambiables)
- **InMemoryVectorStore** para prototipos rápidos
- **Streamlit** para la interfaz web
- **LangSmith** para evaluación automática del sistema

---

## 🗂️ Estructura del repositorio

```
nachabot/
│
├── app.py                  # Aplicación principal en Streamlit
├── load_documents.ipynb    # Indexación de documentos
├── validation/             # Evaluación automática del sistema RAG
├── data/                   # PDFs y URLs de sitios web de admisiones
├── notebooks/              # Notebooks de python exploratorios
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Descripción del proyecto
```

---

## 🚀 Cómo ejecutar localmente

1. **Clonar el repositorio**

```bash
git clone https://github.com/cdtafurd/nachabot.git
cd nachabot
```

2. **Instalar dependencias**

Se recomienda usar un entorno virtual. Luego ejecutar:

```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**

```bash
streamlit run app.py
```

---

## 🧪 Evaluación

El modelo fue evaluado usando métricas estandarizadas para sistemas RAG mediante LangSmith:

- ✅ Correctness (exactitud)
- 📚 Groundedness (fidelidad al contexto)
- 🎯 Relevance (pertinencia)
- 🔍 Retrieval relevance (precisión en recuperación)

Consulta la notebook `validacion_rag.ipynb` para ver los resultados y comparaciones entre `gpt-4o` y `llama3.2`.

---

## 📄 Licencia

Este proyecto es de uso académico y educativo. Para uso institucional, se debe consultar con el autor.

---

## ✍️ Autor

**Cristian Tafur Devia**  
Maestría en Ingeniería de Sistemas y Computación  
Universidad Nacional de Colombia  
[LinkedIn](https://www.linkedin.com/in/cristiantafurdevia/) · [nachabot-dev.streamlit.app](https://nachabot-dev.streamlit.app/)
