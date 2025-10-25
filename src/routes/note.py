from flask import Blueprint, jsonify, request, current_app
from bson.objectid import ObjectId
import datetime
from googletrans import Translator

note_bp = Blueprint('note', __name__)

@note_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes, ordered by most recently updated"""
    mongo = current_app.extensions['pymongo']
    notes = list(mongo.db.notes.find().sort('updated_at', -1))
    for note in notes:
        note['id'] = str(note['_id'])
        del note['_id']
    return jsonify(notes)

@note_bp.route('/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    mongo = current_app.extensions['pymongo']
    data = request.json
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content are required'}), 400
    note = {
        'title': data['title'],
        'content': data['content'],
        # 自动生成当前时间（ISO格式字符串）
        'updated_at': data.get('updated_at') or datetime.datetime.utcnow().isoformat()
    }
    try:
        result = mongo.db.notes.insert_one(note)
        note['id'] = str(result.inserted_id)
        return jsonify(note), 201
    except Exception as e:
        return jsonify({'error': f'Failed to save note: {str(e)}'}), 500

@note_bp.route('/notes/<note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID"""
    mongo = current_app.extensions['pymongo']
    note = mongo.db.notes.find_one({'_id': ObjectId(note_id)})
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    note['id'] = str(note['_id'])
    del note['_id']
    return jsonify(note)

@note_bp.route('/notes/<note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a specific note"""
    mongo = current_app.extensions['pymongo']
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    update_data = {}
    if 'title' in data:
        update_data['title'] = data['title']
    if 'content' in data:
        update_data['content'] = data['content']
    if 'updated_at' in data:
        update_data['updated_at'] = data['updated_at']
    result = mongo.db.notes.update_one({'_id': ObjectId(note_id)}, {'$set': update_data})
    if result.matched_count == 0:
        return jsonify({'error': 'Note not found'}), 404
    note = mongo.db.notes.find_one({'_id': ObjectId(note_id)})
    note['id'] = str(note['_id'])
    del note['_id']
    return jsonify(note)

@note_bp.route('/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a specific note"""
    mongo = current_app.extensions['pymongo']
    result = mongo.db.notes.delete_one({'_id': ObjectId(note_id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Note not found'}), 404
    return '', 204

@note_bp.route('/notes/search', methods=['GET'])
def search_notes():
    """Search notes by title or content"""
    mongo = current_app.extensions['pymongo']
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    notes = list(mongo.db.notes.find({
        '$or': [
            {'title': {'$regex': query, '$options': 'i'}},
            {'content': {'$regex': query, '$options': 'i'}}
        ]
    }).sort('updated_at', -1))
    for note in notes:
        note['id'] = str(note['_id'])
        del note['_id']
    return jsonify(notes)

@note_bp.route('/notes/<note_id>/translate', methods=['POST'])
def translate_note(note_id):
    """
    Translate a note's content to the target language.
    POST body: { "target_lang": "zh-cn" }
    """
    mongo = current_app.extensions['pymongo']
    data = request.json
    target_lang = data.get('target_lang')
    if not target_lang:
        return jsonify({'error': 'target_lang is required'}), 400

    note = mongo.db.notes.find_one({'_id': ObjectId(note_id)})
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    translator = Translator()
    try:
        translated = translator.translate(note['content'], dest=target_lang)
        return jsonify({
            'id': str(note['_id']),
            'title': note['title'],
            'original_content': note['content'],
            'translated_content': translated.text,
            'target_lang': target_lang
        })
    except Exception as e:
        return jsonify({'error': f'Failed to translate: {str(e)}'}), 500

