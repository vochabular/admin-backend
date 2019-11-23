alter table api_chapter drop constraint api_chapter_fk_belongs_to_id_576cd489_fk_api_chapter_id;

alter table api_chapter
	add constraint api_chapter_fk_belongs_to_id_576cd489_fk_api_chapter_id
		foreign key (fk_belongs_to_id) references api_chapter
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_chapter drop constraint api_chapter_fk_book_id_46668b75_fk_api_book_id;

alter table api_chapter
	add constraint api_chapter_fk_book_id_46668b75_fk_api_book_id
		foreign key (fk_book_id) references api_book
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_chaptertitle drop constraint api_chaptertitle_language_id_6c27a0a9_fk_api_language_id;

alter table api_chaptertitle
	add constraint api_chaptertitle_language_id_6c27a0a9_fk_api_language_id
		foreign key (language_id) references api_language
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_chaptertitle drop constraint api_chaptertitle_chapter_id_6db27968_fk_api_chapter_id;

alter table api_chaptertitle
	add constraint api_chaptertitle_chapter_id_6db27968_fk_api_chapter_id
		foreign key (chapter_id) references api_chapter
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_character drop constraint api_character_fk_book_id_ca20a75b_fk_api_book_id;

alter table api_character
	add constraint api_character_fk_book_id_ca20a75b_fk_api_book_id
		foreign key (fk_book_id) references api_book
			on update cascade on delete set null
			deferrable initially deferred;

alter table api_comment drop constraint api_comment_fk_chapter_id_39183f79_fk_api_chapter_id;

alter table api_comment
	add constraint api_comment_fk_chapter_id_39183f79_fk_api_chapter_id
		foreign key (fk_chapter_id) references api_chapter
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_comment drop constraint api_comment_fk_component_id_79fe320e_fk_api_component_id;

alter table api_comment
	add constraint api_comment_fk_component_id_79fe320e_fk_api_component_id
		foreign key (fk_component_id) references api_component
			on update cascade on delete set null
			deferrable initially deferred;

alter table api_comment drop constraint api_comment_fk_parent_comment_id_68b52553_fk_api_comment_id;

alter table api_comment
	add constraint api_comment_fk_parent_comment_id_68b52553_fk_api_comment_id
		foreign key (fk_parent_comment_id) references api_comment
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_component drop constraint api_component_fk_chapter_id_8111705c_fk_api_chapter_id;

alter table api_component
	add constraint api_component_fk_chapter_id_8111705c_fk_api_chapter_id
		foreign key (fk_chapter_id) references api_chapter
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_component drop constraint api_component_fk_component_id_6b3b3166_fk_api_component_id;

alter table api_component
	add constraint api_component_fk_component_id_6b3b3166_fk_api_component_id
		foreign key (fk_component_id) references api_component
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_component drop constraint api_component_fk_component_type_id_7257d108_fk_api_compo;

alter table api_component
	add constraint api_component_fk_component_type_id_7257d108_fk_api_compo
		foreign key (fk_component_type_id) references api_componenttype
			on update cascade on delete restrict
			deferrable initially deferred;

alter table api_component drop constraint api_component_fk_locked_by_id_42c14e1c_fk_api_profile_id;

alter table api_component
	add constraint api_component_fk_locked_by_id_42c14e1c_fk_api_profile_id
		foreign key (fk_locked_by_id) references api_profile
			on update cascade on delete set null
			deferrable initially deferred;

alter table api_componenttype drop constraint api_componenttype_fk_frontend_widget_i_b6515b7e_fk_api_compo;

alter table api_componenttype
	add constraint api_componenttype_fk_frontend_widget_i_b6515b7e_fk_api_compo
		foreign key (fk_frontend_widget_id) references api_componenttype
			on update cascade on delete set null
			deferrable initially deferred;

alter table api_componenttype drop constraint api_componenttype_fk_parent_type_id_17f082de_fk_api_compo;

alter table api_componenttype
	add constraint api_componenttype_fk_parent_type_id_17f082de_fk_api_compo
		foreign key (fk_parent_type_id) references api_componenttype
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_media drop constraint api_media_fk_component_id_73a6dada_fk_api_component_id;

alter table api_media
	add constraint api_media_fk_component_id_73a6dada_fk_api_component_id
		foreign key (fk_component_id) references api_component
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_profile drop constraint api_profile_fk_language_id_7e07e756_fk_api_language_id;

alter table api_profile
	add constraint api_profile_fk_language_id_7e07e756_fk_api_language_id
		foreign key (fk_language_id) references api_language
			on update cascade on delete set null
			deferrable initially deferred;

alter table api_profile drop constraint api_profile_user_id_41309820_fk_auth_user_id;

alter table api_profile
	add constraint api_profile_user_id_41309820_fk_auth_user_id
		foreign key (user_id) references auth_user
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_profile_translator_languages drop constraint api_profile_translat_language_id_b4512bc9_fk_api_langu;

alter table api_profile_translator_languages
	add constraint api_profile_translat_language_id_b4512bc9_fk_api_langu
		foreign key (language_id) references api_language
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_profile_translator_languages drop constraint api_profile_translat_profile_id_04827fb9_fk_api_profi;

alter table api_profile_translator_languages
	add constraint api_profile_translat_profile_id_04827fb9_fk_api_profi
		foreign key (profile_id) references api_profile
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_text drop constraint api_text_fk_component_id_3460180b_fk_api_component_id;

alter table api_text
	add constraint api_text_fk_component_id_3460180b_fk_api_component_id
		foreign key (fk_component_id) references api_component
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_translation drop constraint api_translation_fk_language_id_1d2ccd51_fk_api_language_id;

alter table api_translation
	add constraint api_translation_fk_language_id_1d2ccd51_fk_api_language_id
		foreign key (fk_language_id) references api_language
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_translation drop constraint api_translation_fk_text_id_005e71dc_fk_api_text_id;

alter table api_translation
	add constraint api_translation_fk_text_id_005e71dc_fk_api_text_id
		foreign key (fk_text_id) references api_text
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_wordgroup drop constraint api_wordgroup_fk_chapter_id_6116571e_fk_api_chapter_id;

alter table api_wordgroup
	add constraint api_wordgroup_fk_chapter_id_6116571e_fk_api_chapter_id
		foreign key (fk_chapter_id) references api_chapter
			on update cascade on delete set null
			deferrable initially deferred;

alter table api_wordgroup_words drop constraint api_wordgroup_words_word_id_4d17b2ab_fk_api_word_id;

alter table api_wordgroup_words
	add constraint api_wordgroup_words_word_id_4d17b2ab_fk_api_word_id
		foreign key (word_id) references api_word
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_wordgroup_words drop constraint api_wordgroup_words_wordgroup_id_14408e3a_fk_api_wordgroup_id;

alter table api_wordgroup_words
	add constraint api_wordgroup_words_wordgroup_id_14408e3a_fk_api_wordgroup_id
		foreign key (wordgroup_id) references api_wordgroup
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_wordgrouptitle drop constraint api_wordgrouptitle_language_id_1d5652fe_fk_api_language_id;

alter table api_wordgrouptitle
	add constraint api_wordgrouptitle_language_id_1d5652fe_fk_api_language_id
		foreign key (language_id) references api_language
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_wordgrouptitle drop constraint "api_wordgrouptitle_wordGroup_id_e3edc932_fk_api_wordgroup_id";

alter table api_wordgrouptitle
	add constraint "api_wordgrouptitle_wordGroup_id_e3edc932_fk_api_wordgroup_id"
		foreign key ("wordGroup_id") references api_wordgroup
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_wordtranslation drop constraint api_wordtranslation_fk_language_id_bfc057ff_fk_api_language_id;

alter table api_wordtranslation
	add constraint api_wordtranslation_fk_language_id_bfc057ff_fk_api_language_id
		foreign key (fk_language_id) references api_language
			on update cascade on delete cascade
			deferrable initially deferred;

alter table api_wordtranslation drop constraint api_wordtranslation_word_id_3a712d3e_fk_api_word_id;

alter table api_wordtranslation
	add constraint api_wordtranslation_word_id_3a712d3e_fk_api_word_id
		foreign key (word_id) references api_word
			on update cascade on delete cascade
			deferrable initially deferred;

