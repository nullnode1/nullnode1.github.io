/*
  Yeni yazıları otomatik keşfetmek için sadece bu iki değeri değiştir.
  Örnek: https://github.com/nullnode1/blog-docsify
*/
const BLOG_OWNER = 'nullnode1';
const BLOG_REPO = 'nullnode1.github.io';
const BLOG_BRANCH = 'main';

function postInfo(file) {
  const slug = file.name.replace(/\.md$/i, '');
  const match = slug.match(/^(\d{4})-(\d{2})-(\d{2})-(.+)$/);
  const title = (match ? match[4] : slug)
    .replace(/[-_]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  const date = match ? `${match[3]}.${match[2]}.${match[1]}` : '';
  return { slug, title, date, name: file.name };
}

async function renderBlogPosts() {
  const container = document.getElementById('post-list');
  if (!container) return;

  container.textContent = 'Yazılar yükleniyor…';
  const endpoint = `https://api.github.com/repos/${BLOG_OWNER}/${BLOG_REPO}/contents/posts?ref=${BLOG_BRANCH}`;

  try {
    const response = await fetch(endpoint, {
      headers: { 'Accept': 'application/vnd.github+json' }
    });
    if (!response.ok) {
      if (response.status === 403 || response.status === 429) {
        throw new Error('GitHub API isteği sınırlandı. Bir süre sonra sayfayı yenileyin.');
      }
      throw new Error('Yazılar alınamadı. Depo adını ve posts/ klasörünü kontrol edin.');
    }
    const files = await response.json();
    if (!Array.isArray(files)) throw new Error('GitHub beklenmeyen bir cevap verdi.');

    const posts = files
      .filter(file => file.type === 'file' && /\.md$/i.test(file.name))
      .map(postInfo)
      .sort((a, b) => b.name.localeCompare(a.name, 'tr'));

    if (!container.isConnected) return;
    if (posts.length === 0) {
      container.textContent = 'Henüz yayımlanmış bir yazı yok.';
      return;
    }

    const list = document.createElement('ul');
    list.className = 'post-list';

    for (const post of posts) {
      const item = document.createElement('li');
      item.className = 'post-item';
      const link = document.createElement('a');
      link.href = `#/posts/${encodeURIComponent(post.slug)}`;
      link.textContent = post.title;
      item.append(link);
      if (post.date) {
        const time = document.createElement('time');
        time.className = 'post-date';
        time.dateTime = post.slug.slice(0, 10);
        time.textContent = post.date;
        item.append(time);
      }
      list.append(item);
    }
    container.replaceChildren(list);
  } catch (error) {
    if (!container.isConnected) return;
    container.textContent = error instanceof Error ? error.message : 'Bir hata oluştu.';
    container.className = 'post-error';
  }
}

window.blogPostPlugin = function (hook) {
  hook.doneEach(renderBlogPosts);
};
