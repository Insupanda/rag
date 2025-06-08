import uvicorn

if __name__ == "__main__":
    print("\n=== 보험 상담 챗봇 ===")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
