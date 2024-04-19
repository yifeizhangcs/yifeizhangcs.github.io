<h2 id="publications" style="margin: 2px 0px -15px;">Selected publications and preprints</h2>

<div class="publications">
<ol class="bibliography">

{% for link in site.data.publications.main %}

<li>
<div class="pub-row">
  <div class="col-sm-3 abbr" style="position: relative;padding-right: 15px;padding-left: 15px;">
<!--     {% if link.image %} 
      <img src="{{ link.image }}" class="teaser img-fluid z-depth-1" style="width=100;height=40%">
    {% endif %}     -->

    <style>
    .img-container {
      width: 120px; /* 或者你想要的宽度 */
      height: 120px; /* 或者你想要的高度，保证和宽度一致就可以保持图片比例 */
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: white; /* 多余区域的填充色 */
      overflow: hidden; /* 防止图片溢出容器 */
    }
    
    .img-container img {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain; /* 保证图片内容都显示，且保持原有的宽高比 */
    }
    </style>
    
    <div class="img-container">
      {% if link.image %} 
      <img src="{{ link.image }}" class="teaser img-fluid z-depth-1">
      {% endif %}
    </div>

    {% if link.conference_short %} 
    <abbr class="badge">{{ link.conference_short }}</abbr>
    {% endif %}
  </div>
  <div class="col-sm-9" style="position: relative;padding-right: 15px;padding-left: 20px;">
      <div class="title"><a href="{{ link.pdf }}">{{ link.title }}</a></div>
      <div class="author">{{ link.authors }}</div>
      <div class="periodical"><em>{{ link.conference }}</em>
      </div>
    <div class="links">
      {% if link.pdf %} 
      <a href="{{ link.pdf }}" class="btn btn-sm z-depth-0" role="button" target="_blank" style="font-size:12px;">PDF</a>
      {% endif %}
      {% if link.code %} 
      <a href="{{ link.code }}" class="btn btn-sm z-depth-0" role="button" target="_blank" style="font-size:12px;">Code</a>
      {% endif %}
      {% if link.page %} 
      <a href="{{ link.page }}" class="btn btn-sm z-depth-0" role="button" target="_blank" style="font-size:12px;">Project Page</a>
      {% endif %}
      {% if link.bibtex %} 
      <a href="{{ link.bibtex }}" class="btn btn-sm z-depth-0" role="button" target="_blank" style="font-size:12px;">BibTex</a>
      {% endif %}
      {% if link.notes %} 
      <strong> <i style="color:#e74d3c">{{ link.notes }}</i></strong>
      {% endif %}
      {% if link.others %} 
      {{ link.others }}
      {% endif %}
    </div>
  </div>
</div>
</li>

<br>

{% endfor %}

</ol>
</div>

