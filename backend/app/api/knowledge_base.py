from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.core.database import get_db
from app.models.models import KnowledgeArticle
from app.schemas.schemas import KnowledgeArticleCreate, KnowledgeArticleResponse

router = APIRouter(prefix="/knowledge-base", tags=["Knowledge Base"])

@router.get("", response_model=List[KnowledgeArticleResponse])
def get_articles(
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = db.query(KnowledgeArticle)
    if category:
        q = q.filter(KnowledgeArticle.category == category)
    if search:
        s = f"%{search}%"
        q = q.filter(
            or_(
                KnowledgeArticle.title.ilike(s),
                KnowledgeArticle.problem_summary.ilike(s),
                KnowledgeArticle.resolution.ilike(s),
                KnowledgeArticle.tags.ilike(s)
            )
        )
    return q.order_by(desc(KnowledgeArticle.views_count)).all()

@router.get("/{id}", response_model=KnowledgeArticleResponse)
def get_article_by_id(id: int, db: Session = Depends(get_db)):
    art = db.query(KnowledgeArticle).filter(KnowledgeArticle.id == id).first()
    if not art:
        raise HTTPException(status_code=404, detail="Article not found")
    art.views_count += 1
    db.commit()
    return art

@router.post("/{id}/helpful")
def mark_article_helpful(id: int, db: Session = Depends(get_db)):
    art = db.query(KnowledgeArticle).filter(KnowledgeArticle.id == id).first()
    if not art:
        raise HTTPException(status_code=404, detail="Article not found")
    art.helpful_count += 1
    db.commit()
    return {"status": "success", "helpful_count": art.helpful_count}
