/**
 * Created by lzr on 2019/11/28.
 */
KindEditor.ready(function(K) {
                K.create('textarea[name=detail]',{
                    width : "800px",
                    height : "200px",
                    uploadJson: '/admin/upload/kindeditor',
                });
        });