
Create repo with all params possible:

  $ hg bb_create utst-second --wiki --issues --public --forks=public --descr='Automaticallly made' --language=python
  Creating BitBucket repo Mekk/utst-second
  Repository created
  
  Repository: Mekk/utst-second  (scm: hg, size: *.* kB) (glob)
  Access: public   (owner: Mekk)
  Issues: yes, wiki: yes, forks: public, language: python
  Paths:
      (https)    https://Mekk@bitbucket.org/Mekk/utst-second
      (ssh)      ssh://hg@bitbucket.org/Mekk/utst-second
  Description:
      Automaticallly made
  
  Now `hg push https://bitbucket.org/Mekk/utst-second` to push the code
  Visit https://bitbucket.org/Mekk/utst-second to review details

Checking status:

  $ hg bitbucket_status utst-second 
  Checking status of BitBucket repo utst-second belonging to Mekk
  
  Repository: Mekk/utst-second  (scm: hg, size: *.* kB) (glob)
  Access: public   (owner: Mekk)
  Issues: yes, wiki: yes, forks: public, language: python
  Paths:
      (https)    https://Mekk@bitbucket.org/Mekk/utst-second
      (ssh)      ssh://hg@bitbucket.org/Mekk/utst-second
  Description:
      Automaticallly made

Modifying:

  $ hg bb_modify utst-second --no-wiki --no-issues --private --forks=private
  Applying BitBucket metadata changes (API v1)
  Changes saved
  
  Repository: Mekk/utst-second  (scm: hg, size: *.* kB) (glob)
  Access: private   (owner: Mekk)
  Issues: no, wiki: no, forks: private, language: python
  Paths:
      (https)    https://Mekk@bitbucket.org/Mekk/utst-second
      (ssh)      ssh://hg@bitbucket.org/Mekk/utst-second
  Description:
      Automaticallly made

Cleaning up:

  $ hg bb_delete --force utst-second
  
  Repository: Mekk/utst-second  (scm: hg, size: *.* kB) (glob)
  Access: private   (owner: Mekk)
  Issues: no, wiki: no, forks: private, language: python
  Paths:
      (https)    https://Mekk@bitbucket.org/Mekk/utst-second
      (ssh)      ssh://hg@bitbucket.org/Mekk/utst-second
  Description:
      Automaticallly made
  Deleting BitBucket clone Mekk/utst-second
  BitBucket clone deleted

Verifying whether it is missing:

  $ hg bb_status utst-second
  Checking status of BitBucket repo utst-second belonging to Mekk
  
  Repository Mekk/utst-second does not exist on BitBucket
  [1]

