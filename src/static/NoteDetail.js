import React, { useState } from 'react';

function NoteDetail({ note }) {
  const [translated, setTranslated] = useState('');
  const [loading, setLoading] = useState(false);

  const handleTranslate = async () => {
    setLoading(true);
    setTranslated('');
    try {
      const res = await fetch(`/api/notes/${note.id}/translate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_lang: 'zh-cn' }) // 可根据需要选择语言
      });
      const data = await res.json();
      if (data.translated_content) {
        setTranslated(data.translated_content);
      } else {
        setTranslated(data.error || '翻译失败');
      }
    } catch (e) {
      setTranslated('翻译请求失败');
    }
    setLoading(false);
  };

  return (
    <div>
      {/* ...existing code... */}
      <button onClick={handleTranslate} disabled={loading}>
        {loading ? '翻译中...' : 'AI翻译'}
      </button>
      {translated && (
        <div style={{ marginTop: 10, color: '#007bff' }}>
          <b>翻译结果：</b>{translated}
        </div>
      )}
      {/* ...existing code... */}
    </div>
  );
}

export default NoteDetail;