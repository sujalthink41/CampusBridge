import uvicorn

def run():
    """Run the development server"""
    uvicorn.run(
        "campus_bridge.api.v1.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"]
    )

if __name__ == "__main__":
    run()
