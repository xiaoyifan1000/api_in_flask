# api_in_flask
nyaa_api_in_flask


nayy_run.py web界面，可以直接通过旁边导航获得，或者直接在页面获取

<ul>
                                    <li>按内容查询</li>
                                    <li>按nyaa用户查询</li>
                                    <li>按资源来源是否认证查询</li>
                                    <li>按资源类型查询</li>
                                </ul>
                                <h3>返回格式以及文件</h3>
                                <p>通过查询返回的是xml文本，会编程语言的可以直接进行操作，以下是xml格式说明</p>
                                <p>category Art - Anime 类型<br>
                                    title 鋼鉄の魔女 アンネローゼ／Koutetsu no Majo Annerose [1080p][10bit][English Subbed] 标题 <br>
                                    href /view/3206897 网站实际地址<br>
                                    torrent /download/3206897.torrent 种子下载地址<br>
                                    magnet... 磁力地址<br>
                                    size 2.8 GiB 文件大小<br>
                                    date 2020-12-21 06:46 日期<br>
                                    seeders 64 当前文件源个数<br>
                                    leechers 41当前下载源个数<br>
                                    completed 763 当前完成个数</p>

<h3>api查询说明</h3>

<p>假如我想搜“鋼鉄の魔女”请按照下面格式搜索 /sukebei?search=鋼鉄の魔女<br>返回和nyaa自带的rss很像，返回下载地址和磁力地址，专门方便被墙的兄弟快速下载 如果什么都不填就引用主页</p>

<h3>本站提供一个直接获取torrent文件接口</h3>

<p>在索引页面获取sukebei网站torrent实际地址（比如/download/3206897.torrent）<br>如果是sukebei站点/download2?filename=/download/3206897.torrent<br>如果是nyaa本站文件获取/download?filename=/download/3206897.torrent</p>
<font size="3" color="red">注意：获取指定torrent文件/download是nyaa，/download2是sukebei，混用会导致文件错误问题</font>

<h3>tool文件可以直接调用查询模块，缓存的xml文件在static内</h3>
